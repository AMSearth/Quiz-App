#!/usr/bin/env python
"""
Database restore script for Quiz App
This script restores a backup of the PostgreSQL database used by the Quiz App.
"""

import os
import sys
import subprocess
import argparse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def restore_backup(backup_file, database_url=None):
    """
    Restore a backup of the PostgreSQL database
    
    Args:
        backup_file (str): Path to the backup file
        database_url (str, optional): Database URL. If not provided, it will be read from DATABASE_URL env var
    """
    # Check if backup file exists
    if not os.path.isfile(backup_file):
        print(f"Error: Backup file not found: {backup_file}")
        sys.exit(1)
    
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
    
    # Set environment variables for pg_restore
    env = os.environ.copy()
    env['PGPASSWORD'] = password
    
    # First, drop the existing database (if it exists)
    drop_cmd = [
        'dropdb',
        '-h', host,
        '-p', port,
        '-U', username,
        '--if-exists',
        database_name
    ]
    
    # Then, create a new database
    create_cmd = [
        'createdb',
        '-h', host,
        '-p', port,
        '-U', username,
        database_name
    ]
    
    # Finally, restore the backup
    restore_cmd = [
        'pg_restore',
        '-h', host,
        '-p', port,
        '-U', username,
        '-d', database_name,
        '-v',  # Verbose
        backup_file
    ]
    
    try:
        # Drop existing database
        print(f"Dropping database {database_name} if it exists...")
        subprocess.run(drop_cmd, env=env, check=True, capture_output=True, text=True)
        
        # Create new database
        print(f"Creating database {database_name}...")
        subprocess.run(create_cmd, env=env, check=True, capture_output=True, text=True)
        
        # Restore backup
        print(f"Restoring backup from {backup_file} to {database_name}...")
        result = subprocess.run(restore_cmd, env=env, check=True, capture_output=True, text=True)
        print(f"Restore completed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error restoring backup: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main function to parse arguments and restore backup"""
    parser = argparse.ArgumentParser(description='Restore a backup of the PostgreSQL database')
    parser.add_argument('backup_file', help='Path to the backup file')
    parser.add_argument('--url', '-u', 
                        help='Database URL (default: read from DATABASE_URL env var)')
    
    args = parser.parse_args()
    
    restore_backup(args.backup_file, args.url)

if __name__ == '__main__':
    main() 