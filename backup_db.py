#!/usr/bin/env python
"""
Database backup script for Quiz App
This script creates a backup of the PostgreSQL database used by the Quiz App.
It can be scheduled to run regularly using a cron job or Windows Task Scheduler.
"""

import os
import sys
import datetime
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_backup(backup_dir, database_url=None):
    """
    Create a backup of the PostgreSQL database
    
    Args:
        backup_dir (str): Directory to store the backup
        database_url (str, optional): Database URL. If not provided, it will be read from DATABASE_URL env var
    
    Returns:
        str: Path to the backup file
    """
    # Get database URL from environment if not provided
    if not database_url:
        database_url = os.getenv('DATABASE_URL')
        
    if not database_url:
        print("Error: No DATABASE_URL provided or found in environment variables")
        sys.exit(1)
    
    # Parse database URL
    # Format: postgres://username:password@host:port/database_name
    try:
        # Remove postgres:// prefix
        db_info = database_url.split('://')[1]
        
        # Split credentials and host info
        credentials, host_info = db_info.split('@')
        
        # Get username and password
        username, password = credentials.split(':')
        
        # Get host, port, and database name
        host_port, database_name = host_info.split('/')
        
        # Split host and port if port is specified
        if ':' in host_port:
            host, port = host_port.split(':')
        else:
            host = host_port
            port = '5432'  # Default PostgreSQL port
            
    except Exception as e:
        print(f"Error parsing DATABASE_URL: {e}")
        sys.exit(1)
    
    # Create backup directory if it doesn't exist
    os.makedirs(backup_dir, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_filename = f"{database_name}_backup_{timestamp}.sql"
    backup_path = os.path.join(backup_dir, backup_filename)
    
    # Set environment variables for pg_dump
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    # Build pg_dump command
    cmd = [
        'pg_dump',
        '-h', host,
        '-p', port,
        '-U', username,
        '-F', 'c',  # Custom format (compressed)
        '-b',  # Include large objects
        '-v',  # Verbose
        '-f', backup_path,
        database_name
    ]
    
    try:
        # Execute pg_dump
        print(f"Creating backup of {database_name} to {backup_path}...")
        result = subprocess.run(cmd, env=env, check=True, capture_output=True, text=True)
        print(f"Backup completed successfully: {backup_path}")
        return backup_path
    except subprocess.CalledProcessError as e:
        print(f"Error creating backup: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main function to parse arguments and create backup"""
    parser = argparse.ArgumentParser(description='Create a backup of the PostgreSQL database')
    parser.add_argument('--dir', '-d', default='./backups', 
                        help='Directory to store the backup (default: ./backups)')
    parser.add_argument('--url', '-u', 
                        help='Database URL (default: read from DATABASE_URL env var)')
    
    args = parser.parse_args()
    
    create_backup(args.dir, args.url)

if __name__ == '__main__':
    main() 