from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse, HttpResponseForbidden
from django.utils import timezone
from django.db.models import Q, Count, Avg
from django.urls import reverse
from django.views.decorators.http import require_POST
from .models import UserProfile, Quiz, Question, Choice, QuizAttempt, Answer
from .forms import UserRegistrationForm, QuizForm, QuestionForm, ChoiceFormSet, AnswerForm
import json

def home(request):
    return render(request, 'home.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            try:
                user_profile = UserProfile.objects.get(user=user)
                
                # Check if the user is approved or is an admin
                if user_profile.user_type == 'admin' or user_profile.is_approved:
                    login(request, user)
                    if user_profile.user_type == 'admin':
                        return redirect('admin_dashboard')
                    elif user_profile.user_type == 'teacher':
                        return redirect('teacher_dashboard')
                    else:  # student
                        return redirect('student_dashboard')
                else:
                    if user_profile.approval_status == 'pending':
                        messages.warning(request, "Your account is pending approval from an administrator. Please check back later.")
                    elif user_profile.approval_status == 'rejected':
                        messages.error(request, "Your registration has been rejected. Please contact an administrator for more information.")
                    return redirect('login')
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('login')
        else:
            messages.error(request, "Invalid username or password.")
    
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('home')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            
            # Create user profile with pending status (except for admin)
            approval_status = 'approved' if user_type == 'admin' else 'pending'
            UserProfile.objects.create(
                user=user, 
                user_type=user_type,
                approval_status=approval_status
            )
            
            # Only auto-login admin users
            if user_type == 'admin':
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                return redirect('admin_dashboard')
            else:
                messages.success(request, "Your registration has been submitted and is pending approval from an administrator. You will be notified when your account is approved.")
                return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'register.html', {'form': form})

# Admin views
@login_required
def admin_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    teachers = UserProfile.objects.filter(user_type='teacher')
    students = UserProfile.objects.filter(user_type='student')
    pending_approvals = UserProfile.objects.filter(approval_status='pending').order_by('registration_date')
    
    return render(request, 'admin_dashboard.html', {
        'teachers': teachers,
        'students': students,
        'pending_approvals': pending_approvals
    })

@login_required
def create_user(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_type = form.cleaned_data.get('user_type')
            UserProfile.objects.create(
                user=user, 
                user_type=user_type,
                approval_status='approved'  # Users created by admin are automatically approved
            )
            messages.success(request, f"User {user.username} created successfully.")
            return redirect('admin_dashboard')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'create_user.html', {'form': form})

@login_required
def approve_user(request, user_id):
    admin_profile = get_object_or_404(UserProfile, user=request.user)
    if admin_profile.user_type != 'admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    user_profile = get_object_or_404(UserProfile, user_id=user_id)
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'approve':
            user_profile.approval_status = 'approved'
            messages.success(request, f"User {user_profile.user.username} has been approved.")
        elif action == 'reject':
            user_profile.approval_status = 'rejected'
            messages.warning(request, f"User {user_profile.user.username} has been rejected.")
        
        user_profile.save()
    
    return redirect('admin_dashboard')

@login_required
def edit_user(request, user_id):
    admin_profile = get_object_or_404(UserProfile, user=request.user)
    if admin_profile.user_type != 'admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    user_to_edit = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user_to_edit)
    
    # Only allow editing teachers and students
    if user_profile.user_type == 'admin':
        messages.error(request, "Admin accounts cannot be edited.")
        return redirect('admin_dashboard')
    
    if request.method == 'POST':
        # Update basic user information
        user_to_edit.username = request.POST.get('username')
        user_to_edit.first_name = request.POST.get('first_name')
        user_to_edit.last_name = request.POST.get('last_name')
        user_to_edit.email = request.POST.get('email')
        
        # Update password if provided
        new_password = request.POST.get('new_password')
        if new_password:
            user_to_edit.set_password(new_password)
        
        user_to_edit.save()
        
        # Update user profile
        user_profile.user_type = request.POST.get('user_type')
        user_profile.approval_status = request.POST.get('approval_status')
        user_profile.save()
        
        messages.success(request, f"User {user_to_edit.username} has been updated successfully.")
        return redirect('admin_dashboard')
    
    return render(request, 'edit_user.html', {
        'user_to_edit': user_to_edit,
        'user_profile': user_profile
    })

@login_required
@require_POST
def delete_user(request, user_id):
    admin_profile = get_object_or_404(UserProfile, user=request.user)
    if admin_profile.user_type != 'admin':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    user_to_delete = get_object_or_404(User, id=user_id)
    user_profile = get_object_or_404(UserProfile, user=user_to_delete)
    
    # Only allow deleting teachers and students
    if user_profile.user_type == 'admin':
        messages.error(request, "Admin accounts cannot be deleted.")
        return redirect('admin_dashboard')
    
    username = user_to_delete.username
    user_to_delete.delete()  # This will also delete the associated UserProfile due to CASCADE
    
    messages.success(request, f"User {username} has been deleted successfully.")
    return redirect('admin_dashboard')

# Teacher views
@login_required
def teacher_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher' or not user_profile.is_approved:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quizzes = Quiz.objects.filter(created_by=request.user)
    
    return render(request, 'teacher_dashboard.html', {
        'quizzes': quizzes
    })

@login_required
def create_quiz(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.created_by = request.user
            quiz.save()
            return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        form = QuizForm()
    
    return render(request, 'create_quiz.html', {'form': form})

@login_required
def edit_quiz(request, quiz_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    questions = Question.objects.filter(quiz=quiz)
    
    return render(request, 'edit_quiz.html', {
        'quiz': quiz,
        'questions': questions
    })

@login_required
def add_question(request, quiz_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            question = question_form.save(commit=False)
            question.quiz = quiz
            question.save()
            
            choice_formset = ChoiceFormSet(request.POST, instance=question)
            if choice_formset.is_valid():
                choice_formset.save()
                return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        question_form = QuestionForm()
        choice_formset = ChoiceFormSet()
    
    return render(request, 'add_question.html', {
        'quiz': quiz,
        'question_form': question_form,
        'choice_formset': choice_formset
    })

@login_required
def edit_question(request, question_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz
    
    if quiz.created_by != request.user:
        return HttpResponseForbidden("You don't have permission to edit this question.")
    
    if request.method == 'POST':
        question_form = QuestionForm(request.POST, instance=question)
        if question_form.is_valid():
            question_form.save()
            
            choice_formset = ChoiceFormSet(request.POST, instance=question)
            if choice_formset.is_valid():
                choice_formset.save()
                return redirect('edit_quiz', quiz_id=quiz.id)
    else:
        question_form = QuestionForm(instance=question)
        choice_formset = ChoiceFormSet(instance=question)
    
    return render(request, 'edit_question.html', {
        'quiz': quiz,
        'question': question,
        'question_form': question_form,
        'choice_formset': choice_formset
    })

@login_required
@require_POST
def delete_question(request, question_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    question = get_object_or_404(Question, id=question_id)
    quiz = question.quiz
    
    if quiz.created_by != request.user:
        return HttpResponseForbidden("You don't have permission to delete this question.")
    
    question.delete()
    return redirect('edit_quiz', quiz_id=quiz.id)

@login_required
@require_POST
def publish_quiz(request, quiz_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    quiz.is_published = True
    quiz.save()
    
    return redirect('teacher_dashboard')

# Student views
@login_required
def student_dashboard(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'student' or not user_profile.is_approved:
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    available_quizzes = Quiz.objects.filter(is_published=True)
    attempted_quizzes = QuizAttempt.objects.filter(student=request.user, end_time__isnull=False)
    in_progress_quizzes = QuizAttempt.objects.filter(student=request.user, end_time__isnull=True)
    
    # Filter out quizzes that have been completed
    completed_quiz_ids = attempted_quizzes.values_list('quiz_id', flat=True)
    available_quizzes = available_quizzes.exclude(id__in=completed_quiz_ids)
    
    return render(request, 'student_dashboard.html', {
        'available_quizzes': available_quizzes,
        'attempted_quizzes': attempted_quizzes,
        'in_progress_quizzes': in_progress_quizzes
    })

@login_required
def start_quiz(request, quiz_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'student':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quiz = get_object_or_404(Quiz, id=quiz_id, is_published=True)
    
    # Check if the student has already completed this quiz
    if QuizAttempt.objects.filter(quiz=quiz, student=request.user, end_time__isnull=False).exists():
        messages.error(request, "You have already completed this quiz.")
        return redirect('student_dashboard')
    
    # Check if there's an in-progress attempt
    attempt = QuizAttempt.objects.filter(quiz=quiz, student=request.user, end_time__isnull=True).first()
    
    if not attempt:
        # Create a new attempt
        attempt = QuizAttempt.objects.create(quiz=quiz, student=request.user)
    
    return redirect('take_quiz', attempt_id=attempt.id)

@login_required
def take_quiz(request, attempt_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'student':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    if attempt.end_time:
        return redirect('quiz_result', attempt_id=attempt.id)
    
    quiz = attempt.quiz
    questions = Question.objects.filter(quiz=quiz)
    
    # Get answered questions
    answered_questions = Answer.objects.filter(attempt=attempt).values_list('question_id', flat=True)
    
    # Get the first unanswered question
    current_question = questions.exclude(id__in=answered_questions).first()
    
    if not current_question:
        # All questions answered, finish the quiz
        attempt.end_time = timezone.now()
        attempt.calculate_score()
        attempt.save()
        return redirect('quiz_result', attempt_id=attempt.id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST, question=current_question)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.attempt = attempt
            answer.question = current_question
            answer.save()
            return redirect('take_quiz', attempt_id=attempt.id)
    else:
        form = AnswerForm(question=current_question)
    
    # Calculate time remaining
    time_elapsed = timezone.now() - attempt.start_time
    time_limit_seconds = quiz.time_limit * 60
    time_remaining = max(0, time_limit_seconds - time_elapsed.total_seconds())
    
    return render(request, 'take_quiz.html', {
        'quiz': quiz,
        'attempt': attempt,
        'question': current_question,
        'form': form,
        'question_number': list(questions).index(current_question) + 1,
        'total_questions': questions.count(),
        'time_remaining': time_remaining
    })

@login_required
def quiz_result(request, attempt_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'student':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    if not attempt.end_time:
        return redirect('take_quiz', attempt_id=attempt.id)
    
    answers = Answer.objects.filter(attempt=attempt)
    
    return render(request, 'quiz_result.html', {
        'attempt': attempt,
        'answers': answers
    })

@login_required
@require_POST
def submit_quiz(request, attempt_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'student':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    if not attempt.end_time:
        attempt.end_time = timezone.now()
        attempt.calculate_score()
        attempt.save()
    
    return redirect('quiz_result', attempt_id=attempt.id)

@login_required
@require_POST
def check_time(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    if attempt.end_time:
        return JsonResponse({'redirect': reverse('quiz_result', args=[attempt.id])})
    
    time_elapsed = timezone.now() - attempt.start_time
    time_limit_seconds = attempt.quiz.time_limit * 60
    time_remaining = max(0, time_limit_seconds - time_elapsed.total_seconds())
    
    if time_remaining <= 0:
        attempt.end_time = timezone.now()
        attempt.calculate_score()
        attempt.save()
        return JsonResponse({'redirect': reverse('quiz_result', args=[attempt.id])})
    
    return JsonResponse({'time_remaining': time_remaining})

@login_required
def student_results(request):
    # Check if user is a teacher
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'teacher':
            messages.error(request, "You don't have permission to access this page.")
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('home')
    
    # Get all quizzes created by this teacher
    teacher_quizzes = Quiz.objects.filter(created_by=request.user)
    quiz_ids = teacher_quizzes.values_list('id', flat=True)
    
    # Get all attempts for these quizzes
    attempts = QuizAttempt.objects.filter(quiz_id__in=quiz_ids, end_time__isnull=False).order_by('-end_time')
    
    # Get statistics for each quiz
    quiz_stats = []
    for quiz in teacher_quizzes:
        quiz_attempts = QuizAttempt.objects.filter(quiz=quiz, end_time__isnull=False)
        stats = {
            'quiz': quiz,
            'total_attempts': quiz_attempts.count(),
            'avg_score': quiz_attempts.aggregate(Avg('score'))['score__avg'] or 0,
        }
        quiz_stats.append(stats)
    
    context = {
        'attempts': attempts,
        'quiz_stats': quiz_stats,
    }
    
    return render(request, 'student_results.html', context)

@login_required
def view_student_result(request, attempt_id):
    # Check if user is a teacher
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        if user_profile.user_type != 'teacher':
            messages.error(request, "You don't have permission to access this page.")
            return redirect('home')
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('home')
    
    # Get the attempt and verify it's for a quiz created by this teacher
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    if attempt.quiz.created_by != request.user:
        messages.error(request, "You don't have permission to view this result.")
        return redirect('student_results')
    
    # Get all answers for this attempt
    answers = Answer.objects.filter(attempt=attempt).order_by('question__id')
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'is_teacher_view': True,
    }
    
    return render(request, 'quiz_result.html', context)
