#!/usr/bin/env python
"""
Setup script for Quiz App local development
Run this script on a new PC after cloning the repository
"""

import os
import sys
import subprocess
import getpass
import platform

def run_command(command):
    """Run a shell command and print output"""
    print(f"\n>>> Running: {command}")
    try:
        result = subprocess.run(command, shell=True, text=True)
        if result.returncode != 0:
            print(f"Command failed with exit code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"Error running command: {str(e)}")
        return False

def setup_database():
    """Run migrations to set up the database"""
    print("\n=== Setting up database ===")
    if not run_command("python manage.py migrate"):
        return False
    return True

def create_superuser_manually():
    """Create a superuser account manually"""
    print("\n=== Creating superuser ===")
    username = input("Enter username (default: admin): ") or "admin"
    email = input("Enter email (default: admin@example.com): ") or "admin@example.com"
    
    # Use Django's management command to create superuser
    cmd = f'python manage.py createsuperuser --username {username} --email {email}'
    return run_command(cmd)

def fix_superuser_profiles():
    """Fix superuser profiles using the fix_superuser.py script"""
    print("\n=== Fixing superuser profiles ===")
    
    # Check if fix_superuser.py exists
    if not os.path.exists("fix_superuser.py"):
        print("Creating fix_superuser.py script...")
        with open("fix_superuser.py", "w") as f:
            f.write('''#!/usr/bin/env python
"""
Script to fix superuser accounts that are missing UserProfiles
Run this if you're having trouble logging in with a superuser account
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

# Import models after Django setup
from django.contrib.auth.models import User
from quiz_app.models import UserProfile

def fix_superusers():
    """Create UserProfiles for all superusers that don't have one"""
    print("=== Fixing Superuser Accounts ===")
    
    # Get all superusers
    superusers = User.objects.filter(is_superuser=True)
    
    if not superusers:
        print("No superuser accounts found.")
        return
    
    fixed_count = 0
    already_ok_count = 0
    
    for user in superusers:
        print(f"\nChecking superuser: {user.username}")
        
        # Check if UserProfile exists
        try:
            profile = UserProfile.objects.get(user=user)
            print(f"UserProfile already exists for {user.username}")
            
            # Make sure profile has admin privileges
            if profile.user_type != 'admin' or profile.approval_status != 'approved':
                profile.user_type = 'admin'
                profile.approval_status = 'approved'
                profile.save()
                print(f"Updated UserProfile for {user.username} with admin privileges")
                fixed_count += 1
            else:
                already_ok_count += 1
                
        except UserProfile.DoesNotExist:
            # Create UserProfile
            try:
                profile = UserProfile(
                    user=user,
                    user_type='admin',
                    approval_status='approved'
                )
                profile.save()
                print(f"Created UserProfile for {user.username} with admin privileges")
                fixed_count += 1
            except Exception as e:
                print(f"Error creating UserProfile for {user.username}: {e}")
    
    print("\n=== Summary ===")
    print(f"Total superusers: {superusers.count()}")
    print(f"Fixed accounts: {fixed_count}")
    print(f"Already OK accounts: {already_ok_count}")
    
    if fixed_count > 0:
        print("\nSuperuser accounts have been fixed. You should now be able to log in.")
    else:
        print("\nNo accounts needed fixing. If you're still having login issues, please check:")
        print("1. Are you using the correct username and password?")
        print("2. Is the UserProfile model correctly defined in your models.py?")
        print("3. Are there any other login-related issues in your views.py?")

if __name__ == "__main__":
    fix_superusers()''')
    
    # Run the fix_superuser.py script
    return run_command("python fix_superuser.py")

def check_platform():
    """Check the platform and provide platform-specific instructions"""
    system = platform.system().lower()
    
    if "linux" in system:
        print("\n=== Linux Platform Detected ===")
        print("For Linux-specific setup, please run:")
        print("python fix_linux_errors.py")
        
        # Create fix_linux_errors.py if it doesn't exist
        if not os.path.exists("fix_linux_errors.py"):
            print("Creating fix_linux_errors.py script...")
            with open("fix_linux_errors.py", "w") as f:
                f.write('''#!/usr/bin/env python
"""
Script to fix common Linux-specific errors in the Quiz App
"""

import os
import sys
import django
import subprocess
import platform

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

def run_command(command):
    """Run a shell command and print output"""
    print(f"\n>>> Running: {command}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        return False
    return True

def check_view_functions():
    """Check if all required view functions exist in views.py"""
    print("\n=== Checking View Functions ===")
    
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
    
    missing_functions = []
    for func_name in required_functions:
        if not hasattr(views, func_name):
            missing_functions.append(func_name)
    
    if missing_functions:
        print(f"Missing view functions: {', '.join(missing_functions)}")
        print("This could be causing the ValueError when running the server.")
        
        # Check if we have the latest code
        print("\nChecking if you have the latest code...")
        run_command("git fetch origin")
        run_command("git status")
        
        print("\nYou should pull the latest code with: git pull")
        print("Or manually add the missing view functions to quiz_app/views.py")
    else:
        print("All required view functions exist in views.py")
    
    return len(missing_functions) == 0

def fix_permissions():
    """Fix file permissions for Linux"""
    print("\n=== Fixing File Permissions ===")
    
    # Fix database file permissions
    if os.path.exists("db.sqlite3"):
        run_command("chmod 664 db.sqlite3")
        print("Fixed permissions for db.sqlite3")
    
    # Create and fix permissions for directories
    directories = ["static", "staticfiles", "media"]
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
        
        run_command(f"chmod -R 755 {directory}")
        print(f"Fixed permissions for {directory}")
    
    return True

def check_urls():
    """Check if URLs match view functions"""
    print("\n=== Checking URL Configuration ===")
    
    try:
        from quiz_app.urls import urlpatterns
        from quiz_app import views
        
        for pattern in urlpatterns:
            if hasattr(pattern, 'callback') and pattern.callback:
                callback_name = pattern.callback.__name__
                if not hasattr(views, callback_name):
                    print(f"URL pattern references non-existent view: {callback_name}")
        
        print("URL configuration check completed")
    except Exception as e:
        print(f"Error checking URLs: {str(e)}")
    
    return True

def main():
    """Main function to fix Linux errors"""
    print("=== Quiz App Linux Error Fixer ===")
    print(f"Platform: {platform.platform()}")
    print(f"Python version: {sys.version}")
    print(f"Django version: {django.get_version()}")
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check view functions
    check_view_functions()
    
    # Fix permissions
    fix_permissions()
    
    # Check URLs
    check_urls()
    
    print("\n=== Recommended Commands ===")
    print("1. Pull the latest code:")
    print("   git pull")
    print("\n2. Run the server with proper binding:")
    print("   python manage.py runserver 0.0.0.0:8000")
    print("\n3. If you still have issues, try running with a different port:")
    print("   python manage.py runserver 0.0.0.0:8080")

if __name__ == "__main__":
    main()

def main():
    """Main function to run the setup"""
    print("=== Quiz App Setup ===")
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check platform
    check_platform()
    
    # Install dependencies
    print("\n=== Installing dependencies ===")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install dependencies. Please install them manually.")
    
    # Set up database
    if not setup_database():
        print("Failed to set up database. Please run migrations manually.")
        sys.exit(1)
    
    # Create superuser
    if not create_superuser_manually():
        print("Failed to create superuser. Please create one manually using 'python manage.py createsuperuser'.")
    
    # Fix superuser profiles
    if not fix_superuser_profiles():
        print("Failed to fix superuser profiles. Please run 'python fix_superuser.py' manually.")
    
    # Run the server
    print("\n=== Setup complete! ===")
    print("You can now run the development server with:")
    print("python manage.py runserver")
    
    run_server = input("Would you like to run the server now? (y/n): ").lower() == 'y'
    if run_server:
        if platform.system().lower() == "linux":
            run_command("python manage.py runserver 0.0.0.0:8000")
        else:
            run_command("python manage.py runserver")

if __name__ == "__main__":
    main() 