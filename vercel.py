"""
This file is required by Vercel
It imports the WSGI application from your Django project
"""
import os
import sys

# Add the project directory to the sys.path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")

try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
except Exception as e:
    print(f"Error importing WSGI application: {e}")
    # Create a simple WSGI application that returns the error
    def app(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [f"Error importing WSGI application: {e}".encode()] 