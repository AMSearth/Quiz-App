#!/usr/bin/env python
"""
Local development setup script for Quiz App
This script helps with setting up the local development environment.
"""

import os
import sys
import subprocess
import argparse
import getpass
import random
import string
from pathlib import Path

def create_venv():
    """Create a virtual environment"""
    if os.path.exists('venv'):
        print("Virtual environment already exists")
        return
    
    try:
        print("Creating virtual environment...")
        subprocess.run([sys.executable, '-m', 'venv', 'venv'], check=True)
        print("Virtual environment created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def install_requirements():
    """Install requirements"""
    # Determine the path to the Python executable in the virtual environment
    if os.name == 'nt':  # Windows
        python_path = os.path.join('venv', 'Scripts', 'python.exe')
    else:  # Unix/Linux/Mac
        python_path = os.path.join('venv', 'bin', 'python')
    
    if not os.path.exists(python_path):
        print(f"Error: Virtual environment Python not found at {python_path}")
        print("Please create a virtual environment first")
        sys.exit(1)
    
    try:
        print("Installing requirements...")
        subprocess.run([python_path, '-m', 'pip', 'install', '-r', 'requirements.txt'], check=True)
        print("Requirements installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing requirements: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def create_env_file():
    """Create .env file if it doesn't exist"""
    if os.path.exists('.env'):
        print(".env file already exists")
        return
    
    # Generate a random secret key
    secret_key = ''.join(random.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50))
    
    try:
        print("Creating .env file...")
        with open('.env', 'w') as f:
            f.write(f"DEBUG=True\n")
            f.write(f"SECRET_KEY={secret_key}\n")
            f.write(f"# Add DATABASE_URL if you want to use PostgreSQL locally\n")
            f.write(f"# DATABASE_URL=postgres://username:password@localhost:5432/quiz_app\n")
        print(".env file created successfully")
    except Exception as e:
        print(f"Error creating .env file: {e}")
        sys.exit(1)

def run_migrations(python_path=None):
    """Run migrations"""
    # Determine the path to the Python executable in the virtual environment
    if not python_path:
        if os.name == 'nt':  # Windows
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:  # Unix/Linux/Mac
            python_path = os.path.join('venv', 'bin', 'python')
    
    if not os.path.exists(python_path):
        print(f"Error: Virtual environment Python not found at {python_path}")
        print("Please create a virtual environment first")
        sys.exit(1)
    
    try:
        print("Running migrations...")
        subprocess.run([python_path, 'manage.py', 'migrate'], check=True)
        print("Migrations completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error running migrations: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def create_superuser(python_path=None):
    """Create a superuser"""
    # Determine the path to the Python executable in the virtual environment
    if not python_path:
        if os.name == 'nt':  # Windows
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:  # Unix/Linux/Mac
            python_path = os.path.join('venv', 'bin', 'python')
    
    if not os.path.exists(python_path):
        print(f"Error: Virtual environment Python not found at {python_path}")
        print("Please create a virtual environment first")
        sys.exit(1)
    
    # Get superuser credentials
    username = input("Enter superuser username (default: admin): ") or "admin"
    email = input("Enter superuser email (default: admin@example.com): ") or "admin@example.com"
    password = getpass.getpass("Enter superuser password: ")
    password_confirm = getpass.getpass("Confirm superuser password: ")
    
    if password != password_confirm:
        print("Error: Passwords do not match")
        sys.exit(1)
    
    try:
        print("Creating superuser...")
        # Set environment variables for non-interactive superuser creation
        env = os.environ.copy()
        env['DJANGO_SUPERUSER_PASSWORD'] = password
        
        subprocess.run([
            python_path, 'manage.py', 'createsuperuser',
            '--username', username,
            '--email', email,
            '--noinput'
        ], env=env, check=True)
        
        print(f"Superuser '{username}' created successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error creating superuser: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def collect_static(python_path=None):
    """Collect static files"""
    # Determine the path to the Python executable in the virtual environment
    if not python_path:
        if os.name == 'nt':  # Windows
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:  # Unix/Linux/Mac
            python_path = os.path.join('venv', 'bin', 'python')
    
    if not os.path.exists(python_path):
        print(f"Error: Virtual environment Python not found at {python_path}")
        print("Please create a virtual environment first")
        sys.exit(1)
    
    try:
        print("Collecting static files...")
        subprocess.run([python_path, 'manage.py', 'collectstatic', '--noinput'], check=True)
        print("Static files collected successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error collecting static files: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def run_server(python_path=None):
    """Run the development server"""
    # Determine the path to the Python executable in the virtual environment
    if not python_path:
        if os.name == 'nt':  # Windows
            python_path = os.path.join('venv', 'Scripts', 'python.exe')
        else:  # Unix/Linux/Mac
            python_path = os.path.join('venv', 'bin', 'python')
    
    if not os.path.exists(python_path):
        print(f"Error: Virtual environment Python not found at {python_path}")
        print("Please create a virtual environment first")
        sys.exit(1)
    
    try:
        print("Starting development server...")
        subprocess.run([python_path, 'manage.py', 'runserver'], check=False)
    except KeyboardInterrupt:
        print("\nDevelopment server stopped")
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def setup_all():
    """Run all setup steps"""
    create_venv()
    install_requirements()
    create_env_file()
    
    # Determine the path to the Python executable in the virtual environment
    if os.name == 'nt':  # Windows
        python_path = os.path.join('venv', 'Scripts', 'python.exe')
    else:  # Unix/Linux/Mac
        python_path = os.path.join('venv', 'bin', 'python')
    
    run_migrations(python_path)
    create_superuser(python_path)
    collect_static(python_path)
    
    print("\nSetup completed successfully!")
    print("You can now run the development server with:")
    if os.name == 'nt':  # Windows
        print("venv\\Scripts\\python manage.py runserver")
    else:  # Unix/Linux/Mac
        print("venv/bin/python manage.py runserver")
    
    # Ask if the user wants to start the server now
    start_server = input("\nDo you want to start the development server now? (y/n): ")
    if start_server.lower() == 'y':
        run_server(python_path)

def main():
    """Main function to parse arguments and run commands"""
    parser = argparse.ArgumentParser(description='Local development setup script for Quiz App')
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Setup command
    setup_parser = subparsers.add_parser('setup', help='Run all setup steps')
    
    # Venv command
    venv_parser = subparsers.add_parser('venv', help='Create a virtual environment')
    
    # Install command
    install_parser = subparsers.add_parser('install', help='Install requirements')
    
    # Env command
    env_parser = subparsers.add_parser('env', help='Create .env file')
    
    # Migrate command
    migrate_parser = subparsers.add_parser('migrate', help='Run migrations')
    
    # Superuser command
    superuser_parser = subparsers.add_parser('createsuperuser', help='Create a superuser')
    
    # Collectstatic command
    collectstatic_parser = subparsers.add_parser('collectstatic', help='Collect static files')
    
    # Runserver command
    runserver_parser = subparsers.add_parser('runserver', help='Run the development server')
    
    args = parser.parse_args()
    
    # Run the appropriate command
    if args.command == 'setup':
        setup_all()
    elif args.command == 'venv':
        create_venv()
    elif args.command == 'install':
        install_requirements()
    elif args.command == 'env':
        create_env_file()
    elif args.command == 'migrate':
        run_migrations()
    elif args.command == 'createsuperuser':
        create_superuser()
    elif args.command == 'collectstatic':
        collect_static()
    elif args.command == 'runserver':
        run_server()
    else:
        # If no command is provided, run setup
        setup_all()

if __name__ == '__main__':
    main() 