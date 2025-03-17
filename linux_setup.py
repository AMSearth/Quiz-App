#!/usr/bin/env python
"""
Setup script for Quiz App on Linux environments
This script helps with common Linux-specific setup issues
"""

import os
import sys
import subprocess
import django
import platform

def run_command(command):
    """Run a shell command and print output"""
    print(f"\n>>> Running: {command}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        print(f"Command failed with exit code {result.returncode}")
        return False
    return True

def check_environment():
    """Check the environment and print system information"""
    print("\n=== System Information ===")
    print(f"Platform: {platform.platform()}")
    print(f"Python version: {sys.version}")
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
    django.setup()
    
    print(f"Django version: {django.get_version()}")
    
    # Check for common Linux dependencies
    print("\n=== Checking Dependencies ===")
    dependencies = [
        "sqlite3 --version",
        "which python3",
        "which pip3",
        "ls -la /var/run/",  # Check for socket permissions
    ]
    
    for cmd in dependencies:
        run_command(cmd)
    
    return True

def fix_permissions():
    """Fix common Linux permission issues"""
    print("\n=== Fixing Permissions ===")
    
    # Fix database file permissions
    if os.path.exists("db.sqlite3"):
        run_command("chmod 664 db.sqlite3")
        run_command("ls -la db.sqlite3")
    
    # Fix directory permissions
    directories = ["static", "staticfiles", "media"]
    for directory in directories:
        if os.path.exists(directory):
            run_command(f"chmod -R 755 {directory}")
    
    # Create directories if they don't exist
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            print(f"Created directory: {directory}")
    
    return True

def fix_socket_issues():
    """Fix common socket issues on Linux"""
    print("\n=== Checking for Socket Issues ===")
    
    # Check if we can bind to the port
    run_command("netstat -tuln | grep 8000")
    
    # Suggest alternative port if 8000 is in use
    print("\nIf port 8000 is in use, try running the server on a different port:")
    print("python manage.py runserver 8080")
    
    return True

def main():
    """Main function to run the setup"""
    print("=== Quiz App Linux Setup ===")
    
    # Check if we're in the right directory
    if not os.path.exists("manage.py"):
        print("Error: manage.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Check environment
    check_environment()
    
    # Fix permissions
    fix_permissions()
    
    # Fix socket issues
    fix_socket_issues()
    
    # Run migrations
    print("\n=== Running Migrations ===")
    run_command("python manage.py migrate")
    
    # Collect static files
    print("\n=== Collecting Static Files ===")
    run_command("python manage.py collectstatic --noinput")
    
    # Run the server
    print("\n=== Setup Complete! ===")
    print("You can now run the development server with:")
    print("python manage.py runserver 0.0.0.0:8000")
    
    run_server = input("Would you like to run the server now? (y/n): ").lower() == 'y'
    if run_server:
        run_command("python manage.py runserver 0.0.0.0:8000")

if __name__ == "__main__":
    main() 