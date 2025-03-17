#!/usr/bin/env python
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
    
    print("\nFor more detailed troubleshooting, see LINUX_TROUBLESHOOTING.md")

if __name__ == "__main__":
    main() 