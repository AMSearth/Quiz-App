import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

print("Starting Vercel setup...")

# Create staticfiles directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'staticfiles'), exist_ok=True)
print("Created staticfiles directory")

# Create static directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)
print("Created static directory")

# Create a simple CSS file to ensure static files are working
css_dir = os.path.join(BASE_DIR, 'static', 'css')
os.makedirs(css_dir, exist_ok=True)

# Create a simple test file to verify static files are working
with open(os.path.join(css_dir, 'vercel-test.css'), 'w') as f:
    f.write('/* This file was created by vercel_setup.py */\n')
    f.write('body { background-color: #f0f0f0; }\n')

print("Created test CSS file")

# Create a simple favicon to prevent 404 errors
favicon_path = os.path.join(BASE_DIR, 'static', 'favicon.ico')
if not os.path.exists(favicon_path):
    try:
        # Create a minimal 16x16 favicon
        with open(favicon_path, 'wb') as f:
            # Simple 16x16 transparent ICO file (hex data)
            ico_data = bytes.fromhex(
                '00000100010010100000010020006804000016000000280000001000'
                '0000200000000100200000000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000'
                '0000000000000000000000000000000000000000000000000000000000'
            )
            f.write(ico_data)
        print("Created favicon.ico")
    except Exception as e:
        print(f"Error creating favicon: {e}")

print("Vercel setup completed successfully!") 