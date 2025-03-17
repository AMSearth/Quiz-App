#!/usr/bin/env python
"""
Setup script for Quiz App local development
Run this script on a new PC after cloning the repository
"""

import os
import sys
import subprocess
import getpass
import django
from django.core.management import call_command

def run_command(command):
    """Run a shell command and print output"""
    print(f"\n>>> Running: {command}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        return False
    return True

def setup_database():
    """Run migrations to set up the database"""
    print("\n=== Setting up database ===")
    if not run_command("python manage.py migrate"):
        return False
    return True

def create_superuser_with_profile():
    """Create a superuser account with UserProfile"""
    print("\n=== Creating superuser with UserProfile ===")
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
    django.setup()
    
    # Import models after Django setup
    from django.contrib.auth.models import User
    from quiz_app.models import UserProfile
    
    # Get superuser details
    username = input("Enter username (default: admin): ") or "admin"
    email = input("Enter email (default: admin@example.com): ") or "admin@example.com"
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        print(f"User '{username}' already exists.")
        user = User.objects.get(username=username)
    else:
        # Create superuser using management command
        print(f"Creating superuser '{username}'...")
        try:
            # Use subprocess to handle password input securely
            cmd = f'python manage.py createsuperuser --username {username} --email {email}'
            if not run_command(cmd):
                return False
            
            # Get the created user
            user = User.objects.get(username=username)
        except Exception as e:
            print(f"Error creating superuser: {e}")
            return False
    
    # Create or update UserProfile
    try:
        # Check if profile exists
        profile, created = UserProfile.objects.get_or_create(user=user)
        
        if created:
            # Set profile attributes for new profile
            profile.user_type = 'admin'
            profile.approval_status = 'approved'
            profile.save()
            print(f"Created UserProfile for '{username}' with admin privileges")
        else:
            # Update existing profile
            profile.user_type = 'admin'
            profile.approval_status = 'approved'
            profile.save()
            print(f"Updated UserProfile for '{username}' with admin privileges")
        
        return True
    except Exception as e:
        print(f"Error creating UserProfile: {e}")
        print("This might be because the UserProfile model is not properly defined.")
        print("Please check your models.py file and make sure UserProfile has the correct fields.")
        return False

def main():
    """Main function to run the setup"""
    print("=== Quiz App Setup ===")
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install dependencies
    print("\n=== Installing dependencies ===")
    if not run_command("pip install -r requirements.txt"):
        print("Failed to install dependencies. Please install them manually.")
    
    # Set up database
    if not setup_database():
        print("Failed to set up database. Please run migrations manually.")
        sys.exit(1)
    
    # Create superuser with profile
    if not create_superuser_with_profile():
        print("Failed to create superuser with profile. Please check the error messages above.")
    
    # Run the server
    print("\n=== Setup complete! ===")
    print("You can now run the development server with:")
    print("python manage.py runserver")
    
    run_server = input("Would you like to run the server now? (y/n): ").lower() == 'y'
    if run_server:
        run_command("python manage.py runserver")

if __name__ == "__main__":
    main() 