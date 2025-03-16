#!/usr/bin/env python
"""
Vercel database migration script for Quiz App
This script helps with running database migrations on Vercel.
It can be used with the Vercel CLI to run migrations after deployment.
"""

import os
import sys
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_migrations():
    """Run Django migrations"""
    try:
        print("Running migrations...")
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def create_superuser(username, email, password=None):
    """
    Create a superuser
    
    Args:
        username (str): Superuser username
        email (str): Superuser email
        password (str, optional): Superuser password. If not provided, it will be prompted
    """
    try:
        # Check if the user already exists
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        if User.objects.filter(username=username).exists():
            print(f"User '{username}' already exists")
            return
        
        # Create the superuser
        if password:
            # Create superuser non-interactively
            os.environ['DJANGO_SUPERUSER_PASSWORD'] = password
            subprocess.run([
                sys.executable, 'manage.py', 'createsuperuser',
                '--username', username,
                '--email', email,
                '--noinput'
            ], check=True)
        else:
            # Create superuser interactively
            subprocess.run([
                sys.executable, 'manage.py', 'createsuperuser',
                '--username', username,
                '--email', email
            ], check=True)
            
        print(f"Superuser '{username}' created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error creating superuser: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def collect_static():
    """Collect static files"""
    try:
        print("Collecting static files...")
        subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("Static files collected successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error collecting static files: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main function to parse arguments and run commands"""
    parser = argparse.ArgumentParser(description='Vercel database migration script for Quiz App')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Run migrations')
    
    # Superuser command
    superuser_parser = subparsers.add_parser('createsuperuser', help='Create a superuser')
    superuser_parser.add_argument('--username', '-u', required=True, help='Superuser username')
    superuser_parser.add_argument('--email', '-e', required=True, help='Superuser email')
    superuser_parser.add_argument('--password', '-p', help='Superuser password (optional)')
    
    # Collectstatic command
    collectstatic_parser = subparsers.add_parser('collectstatic', help='Collect static files')
    
    args = parser.parse_args()
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
    
    # Import Django and set up
    import django
    django.setup()
    
    # Run the appropriate command
    if args.command == 'migrate':
        run_migrations()
    elif args.command == 'createsuperuser':
        create_superuser(args.username, args.email, args.password)
    elif args.command == 'collectstatic':
        collect_static()
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main() 