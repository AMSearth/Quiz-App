import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.contrib.auth.models import User
from quiz_app.models import UserProfile

def create_admin_user():
    # Create a superuser
    username = 'admin'
    email = 'admin@example.com'
    password = 'admin123'
    
    try:
        # Check if user already exists
        user = User.objects.get(username=username)
        print(f"User {username} already exists.")
    except User.DoesNotExist:
        # Create the user
        user = User.objects.create_superuser(username=username, email=email, password=password)
        print(f"Superuser {username} created successfully.")
    
    # Create or get UserProfile with admin type
    profile, created = UserProfile.objects.get_or_create(
        user=user,
        defaults={'user_type': 'admin'}
    )
    
    if created:
        print(f"Admin profile created for {username}")
    else:
        print(f"Admin profile already exists for {username}")
    
    # Create a teacher user
    teacher_username = 'teacher'
    teacher_email = 'teacher@example.com'
    teacher_password = 'teacher123'
    
    try:
        teacher = User.objects.get(username=teacher_username)
        print(f"User {teacher_username} already exists.")
    except User.DoesNotExist:
        teacher = User.objects.create_user(username=teacher_username, email=teacher_email, password=teacher_password)
        print(f"User {teacher_username} created successfully.")
    
    teacher_profile, created = UserProfile.objects.get_or_create(
        user=teacher,
        defaults={'user_type': 'teacher'}
    )
    
    if created:
        print(f"Teacher profile created for {teacher_username}")
    else:
        print(f"Teacher profile already exists for {teacher_username}")
    
    # Create a student user
    student_username = 'student'
    student_email = 'student@example.com'
    student_password = 'student123'
    
    try:
        student = User.objects.get(username=student_username)
        print(f"User {student_username} already exists.")
    except User.DoesNotExist:
        student = User.objects.create_user(username=student_username, email=student_email, password=student_password)
        print(f"User {student_username} created successfully.")
    
    student_profile, created = UserProfile.objects.get_or_create(
        user=student,
        defaults={'user_type': 'student'}
    )
    
    if created:
        print(f"Student profile created for {student_username}")
    else:
        print(f"Student profile already exists for {student_username}")

if __name__ == "__main__":
    create_admin_user() 