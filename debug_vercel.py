import os
import sys
import django
from django.conf import settings

# Print Python version and environment
print(f"Python version: {sys.version}")
print(f"Django version: {django.__version__}")
print("\nEnvironment variables:")
for key, value in os.environ.items():
    # Don't print sensitive values
    if 'SECRET' in key or 'PASSWORD' in key or 'TOKEN' in key:
        print(f"{key}: [REDACTED]")
    else:
        print(f"{key}: {value}")

# Try to import required modules
try:
    import dj_database_url
    print("\ndj-database-url is installed correctly")
except ImportError:
    print("\nERROR: dj-database-url is not installed")

try:
    from dotenv import load_dotenv
    print("python-dotenv is installed correctly")
except ImportError:
    print("ERROR: python-dotenv is not installed")

try:
    import whitenoise
    print("whitenoise is installed correctly")
except ImportError:
    print("ERROR: whitenoise is not installed")

try:
    import psycopg2
    print("psycopg2-binary is installed correctly")
except ImportError:
    print("ERROR: psycopg2-binary is not installed")

# Check if DATABASE_URL is set
if 'DATABASE_URL' in os.environ:
    print("\nDATABASE_URL is set")
    # Try to parse it
    try:
        config = dj_database_url.parse(os.environ.get('DATABASE_URL'))
        print("DATABASE_URL parsed successfully")
        # Don't print the actual config as it contains sensitive information
    except Exception as e:
        print(f"Error parsing DATABASE_URL: {str(e)}")
else:
    print("\nWARNING: DATABASE_URL is not set")

print("\nChecking for static files directory:")
static_root = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
if os.path.exists(static_root):
    print(f"Static root directory exists at: {static_root}")
    print(f"Contents: {os.listdir(static_root)}")
else:
    print(f"Static root directory does not exist at: {static_root}")

print("\nDebug information complete") 