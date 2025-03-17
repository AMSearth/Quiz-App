from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Quiz, Question, Choice, Answer, QuizAttempt

class UserRegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ['title', 'description', 'time_limit', 'is_published']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3}),
        }

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['text', 'is_correct']

ChoiceFormSet = forms.inlineformset_factory(
    Question, Choice, form=ChoiceForm, extra=4, can_delete=True, min_num=2, validate_min=True
)

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['selected_choice']
        widgets = {
            'selected_choice': forms.RadioSelect(),
        }
    
    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question', None)
        super().__init__(*args, **kwargs)
        
        if question:
            self.fields['selected_choice'].queryset = question.choices.all()
            self.fields['selected_choice'].label = question.text 