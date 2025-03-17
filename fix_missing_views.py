#!/usr/bin/env python
"""
Script to fix missing view functions in the Quiz App
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

def add_missing_views():
    """Add missing view functions to views.py"""
    print("=== Adding Missing View Functions ===")
    
    # Import views module
    from quiz_app import views
    
    # List of required view functions
    required_functions = [
        'home', 'user_login', 'user_logout', 'register',
        'admin_dashboard', 'create_user', 'approve_user', 'edit_user', 'delete_user',
        'teacher_dashboard', 'create_quiz', 'edit_quiz', 'delete_quiz',
        'add_question', 'edit_question', 'delete_question', 'publish_quiz',
        'quiz_results', 'student_results', 'view_student_result',
        'student_dashboard', 'start_quiz', 'take_quiz', 'submit_quiz',
        'quiz_result', 'check_time'
    ]
    
    # Check which functions are missing
    missing_functions = []
    for func_name in required_functions:
        if not hasattr(views, func_name):
            missing_functions.append(func_name)
    
    if not missing_functions:
        print("All required view functions exist. No changes needed.")
        return True
    
    print(f"Missing view functions: {', '.join(missing_functions)}")
    
    # Add missing view functions
    views_file_path = os.path.join('quiz_app', 'views.py')
    
    # Read the current views.py file
    with open(views_file_path, 'r') as f:
        views_content = f.read()
    
    # Add missing functions
    new_functions = []
    
    if 'delete_quiz' in missing_functions:
        new_functions.append("""
@login_required
@require_POST
def delete_quiz(request, quiz_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    quiz.delete()
    
    messages.success(request, f"Quiz '{quiz.title}' has been deleted successfully.")
    return redirect('teacher_dashboard')
""")
    
    if 'quiz_results' in missing_functions:
        new_functions.append("""
@login_required
def quiz_results(request, quiz_id):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if user_profile.user_type != 'teacher':
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    quiz = get_object_or_404(Quiz, id=quiz_id, created_by=request.user)
    attempts = QuizAttempt.objects.filter(quiz=quiz, end_time__isnull=False).order_by('-end_time')
    
    # Calculate statistics
    total_attempts = attempts.count()
    avg_score = attempts.aggregate(Avg('score'))['score__avg'] or 0
    
    context = {
        'quiz': quiz,
        'attempts': attempts,
        'total_attempts': total_attempts,
        'avg_score': avg_score,
    }
    
    return render(request, 'quiz_results.html', context)
""")
    
    if 'check_time' in missing_functions:
        new_functions.append("""
@login_required
def check_time(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id, student=request.user)
    
    # Calculate time elapsed and time remaining
    time_elapsed = timezone.now() - attempt.start_time
    time_limit_seconds = attempt.quiz.time_limit * 60
    time_remaining_seconds = max(0, time_limit_seconds - time_elapsed.total_seconds())
    
    # Convert to minutes and seconds
    minutes = int(time_remaining_seconds // 60)
    seconds = int(time_remaining_seconds % 60)
    
    return JsonResponse({
        'time_elapsed': int(time_elapsed.total_seconds()),
        'time_remaining': int(time_remaining_seconds),
        'time_remaining_formatted': f"{minutes}:{seconds:02d}",
        'is_time_up': time_remaining_seconds <= 0
    })
""")
    
    if 'quiz_result' in missing_functions:
        new_functions.append("""
@login_required
def quiz_result(request, attempt_id):
    attempt = get_object_or_404(QuizAttempt, id=attempt_id)
    
    # Check if the user is the student who took the quiz or the teacher who created it
    user_profile = get_object_or_404(UserProfile, user=request.user)
    if request.user != attempt.student and (user_profile.user_type != 'teacher' or request.user != attempt.quiz.created_by):
        return HttpResponseForbidden("You don't have permission to view this result.")
    
    # Get all answers for this attempt
    answers = Answer.objects.filter(attempt=attempt).order_by('question__id')
    
    context = {
        'attempt': attempt,
        'answers': answers,
        'is_teacher_view': request.user == attempt.quiz.created_by,
    }
    
    return render(request, 'quiz_result.html', context)
""")
    
    # Add the new functions to the views.py file
    if new_functions:
        with open(views_file_path, 'a') as f:
            f.write("\n# Added by fix_missing_views.py\n")
            for func in new_functions:
                f.write(func)
        
        print(f"Added {len(new_functions)} missing view functions to views.py")
    
    return True

def create_missing_templates():
    """Create missing template files"""
    print("\n=== Creating Missing Templates ===")
    
    # Check if quiz_results.html exists
    templates_dir = 'templates'
    quiz_results_path = os.path.join(templates_dir, 'quiz_results.html')
    
    if not os.path.exists(quiz_results_path):
        print("Creating quiz_results.html template...")
        
        # Create the templates directory if it doesn't exist
        if not os.path.exists(templates_dir):
            os.makedirs(templates_dir)
        
        # Create the quiz_results.html file
        with open(quiz_results_path, 'w') as f:
            f.write("""{% extends 'base.html' %}

{% block title %}Quiz Results - {{ quiz.title }}{% endblock %}

{% block content %}
<div class="container mt-4">
    <div class="row">
        <div class="col-12">
            <nav aria-label="breadcrumb">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="{% url 'teacher_dashboard' %}">Teacher Dashboard</a></li>
                    <li class="breadcrumb-item active" aria-current="page">Quiz Results</li>
                </ol>
            </nav>
            
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h4 class="mb-0">Results for: {{ quiz.title }}</h4>
                </div>
                <div class="card-body">
                    <div class="row mb-4">
                        <div class="col-md-4">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Total Attempts</h5>
                                    <h2 class="display-4">{{ total_attempts }}</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Average Score</h5>
                                    <h2 class="display-4">{{ avg_score|floatformat:1 }}%</h2>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-4">
                            <div class="card bg-light">
                                <div class="card-body text-center">
                                    <h5 class="card-title">Quiz Status</h5>
                                    <h2 class="display-4">
                                        {% if quiz.is_published %}
                                            <span class="badge bg-success">Published</span>
                                        {% else %}
                                            <span class="badge bg-warning">Draft</span>
                                        {% endif %}
                                    </h2>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <h5 class="mb-3">Student Attempts</h5>
                    
                    {% if attempts %}
                        <div class="table-responsive">
                            <table class="table table-striped table-hover">
                                <thead class="table-dark">
                                    <tr>
                                        <th>Student</th>
                                        <th>Date Completed</th>
                                        <th>Score</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {% for attempt in attempts %}
                                        <tr>
                                            <td>{{ attempt.student.username }}</td>
                                            <td>{{ attempt.end_time|date:"M d, Y H:i" }}</td>
                                            <td>
                                                <div class="progress">
                                                    <div class="progress-bar {% if attempt.score >= 70 %}bg-success{% elif attempt.score >= 40 %}bg-warning{% else %}bg-danger{% endif %}" 
                                                         role="progressbar" 
                                                         style="width: {{ attempt.score }}%" 
                                                         aria-valuenow="{{ attempt.score }}" 
                                                         aria-valuemin="0" 
                                                         aria-valuemax="100">
                                                        {{ attempt.score|floatformat:1 }}%
                                                    </div>
                                                </div>
                                            </td>
                                            <td>
                                                <a href="{% url 'view_student_result' attempt.id %}" class="btn btn-sm btn-primary">
                                                    <i class="bi bi-eye"></i> View Details
                                                </a>
                                            </td>
                                        </tr>
                                    {% endfor %}
                                </tbody>
                            </table>
                        </div>
                    {% else %}
                        <div class="alert alert-info">
                            No students have completed this quiz yet.
                        </div>
                    {% endif %}
                </div>
            </div>
            
            <div class="d-flex justify-content-between">
                <a href="{% url 'teacher_dashboard' %}" class="btn btn-secondary">
                    <i class="bi bi-arrow-left"></i> Back to Dashboard
                </a>
                <a href="{% url 'edit_quiz' quiz.id %}" class="btn btn-primary">
                    <i class="bi bi-pencil"></i> Edit Quiz
                </a>
            </div>
        </div>
    </div>
</div>
{% endblock %}""")
        
        print("Created quiz_results.html template")
    
    return True

def main():
    """Main function to fix missing views"""
    print("=== Quiz App Missing Views Fixer ===")
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Add missing view functions
    add_missing_views()
    
    # Create missing templates
    create_missing_templates()
    
    print("\n=== Fix Complete ===")
    print("You should now be able to run the server without errors.")
    print("Run the server with:")
    print("python manage.py runserver")
    
    return True

if __name__ == "__main__":
    main() 