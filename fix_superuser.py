#!/usr/bin/env python
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
    fix_superusers() 