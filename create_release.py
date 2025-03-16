#!/usr/bin/env python
"""
Release creation script for Quiz App
This script helps with creating a new release of the Quiz App.
It updates version numbers, creates a changelog, and tags the release.
"""

import os
import sys
import subprocess
import argparse
import datetime
import re
from pathlib import Path

def get_current_version():
    """Get the current version from the README file"""
    try:
        # Try to find version in README.md
        if os.path.exists('README.md'):
            with open('README.md', 'r') as f:
                content = f.read()
                match = re.search(r'Version: (\d+\.\d+\.\d+)', content)
                if match:
                    return match.group(1)
        
        # If not found, check if there's a VERSION file
        if os.path.exists('VERSION'):
            with open('VERSION', 'r') as f:
                return f.read().strip()
        
        # If no version found, return 0.1.0
        return '0.1.0'
    except Exception as e:
        print(f"Error getting current version: {e}")
        return '0.1.0'

def update_version(version_type):
    """
    Update the version number
    
    Args:
        version_type (str): Type of version update (major, minor, patch)
    
    Returns:
        str: New version number
    """
    current_version = get_current_version()
    major, minor, patch = map(int, current_version.split('.'))
    
    if version_type == 'major':
        major += 1
        minor = 0
        patch = 0
    elif version_type == 'minor':
        minor += 1
        patch = 0
    elif version_type == 'patch':
        patch += 1
    
    new_version = f"{major}.{minor}.{patch}"
    
    # Update VERSION file
    with open('VERSION', 'w') as f:
        f.write(new_version)
    
    # Update README.md if it has a version
    if os.path.exists('README.md'):
        with open('README.md', 'r') as f:
            content = f.read()
        
        if re.search(r'Version: (\d+\.\d+\.\d+)', content):
            content = re.sub(r'Version: (\d+\.\d+\.\d+)', f'Version: {new_version}', content)
            with open('README.md', 'w') as f:
                f.write(content)
        else:
            # Add version to README if it doesn't exist
            with open('README.md', 'r') as f:
                lines = f.readlines()
            
            # Find the first heading
            for i, line in enumerate(lines):
                if line.startswith('# '):
                    # Insert version after the first heading
                    lines.insert(i + 1, f'\nVersion: {new_version}\n\n')
                    break
            
            with open('README.md', 'w') as f:
                f.writelines(lines)
    
    return new_version

def get_changes_since_last_tag():
    """Get the changes since the last tag"""
    try:
        # Get the last tag
        last_tag = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], 
                                  capture_output=True, text=True)
        
        if last_tag.returncode != 0:
            # No tags found, get all commits
            changes = subprocess.run(['git', 'log', '--pretty=format:%h %s'], 
                                     capture_output=True, text=True)
        else:
            # Get commits since last tag
            changes = subprocess.run(['git', 'log', f'{last_tag.stdout.strip()}..HEAD', '--pretty=format:%h %s'], 
                                     capture_output=True, text=True)
        
        return changes.stdout.strip()
    except Exception as e:
        print(f"Error getting changes: {e}")
        return ""

def create_changelog(version, changes):
    """
    Create a changelog entry
    
    Args:
        version (str): Version number
        changes (str): Changes since last tag
    """
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    
    # Create CHANGELOG.md if it doesn't exist
    if not os.path.exists('CHANGELOG.md'):
        with open('CHANGELOG.md', 'w') as f:
            f.write('# Changelog\n\n')
    
    # Read existing changelog
    with open('CHANGELOG.md', 'r') as f:
        content = f.read()
    
    # Add new entry
    entry = f"## {version} ({today})\n\n"
    
    if changes:
        # Format changes as a list
        changes_list = [f"- {line}" for line in changes.split('\n')]
        entry += '\n'.join(changes_list) + '\n\n'
    else:
        entry += "- No changes recorded\n\n"
    
    # Add entry after the header
    content = content.replace('# Changelog\n\n', f'# Changelog\n\n{entry}')
    
    # Write updated changelog
    with open('CHANGELOG.md', 'w') as f:
        f.write(content)

def tag_release(version, message=None):
    """
    Tag the release
    
    Args:
        version (str): Version number
        message (str, optional): Tag message
    """
    if not message:
        message = f"Release {version}"
    
    try:
        # Create an annotated tag
        subprocess.run(['git', 'tag', '-a', f'v{version}', '-m', message], check=True)
        print(f"Tagged release v{version}")
    except subprocess.CalledProcessError as e:
        print(f"Error tagging release: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main():
    """Main function to parse arguments and create a release"""
    parser = argparse.ArgumentParser(description='Release creation script for Quiz App')
    parser.add_argument('version_type', choices=['major', 'minor', 'patch'],
                        help='Type of version update')
    parser.add_argument('--message', '-m', help='Release message')
    parser.add_argument('--no-tag', action='store_true', help='Do not tag the release')
    
    args = parser.parse_args()
    
    # Check if git is available
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
    except:
        print("Error: Git is not installed or not in PATH")
        sys.exit(1)
    
    # Check if we're in a git repository
    try:
        subprocess.run(['git', 'rev-parse', '--is-inside-work-tree'], check=True, capture_output=True)
    except:
        print("Error: Not in a git repository")
        sys.exit(1)
    
    # Update version
    new_version = update_version(args.version_type)
    print(f"Updated version to {new_version}")
    
    # Get changes
    changes = get_changes_since_last_tag()
    
    # Create changelog
    create_changelog(new_version, changes)
    print(f"Updated CHANGELOG.md")
    
    # Tag release
    if not args.no_tag:
        tag_release(new_version, args.message)
    
    print(f"\nRelease {new_version} created successfully!")
    print(f"Don't forget to push the changes and tags:")
    print(f"  git push origin master")
    print(f"  git push --tags")

if __name__ == '__main__':
    main() 