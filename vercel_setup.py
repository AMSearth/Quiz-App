import os
import sys
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent

# Create staticfiles directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'staticfiles'), exist_ok=True)

# Create static directory if it doesn't exist
os.makedirs(os.path.join(BASE_DIR, 'static'), exist_ok=True)

print("Vercel setup completed successfully!") 