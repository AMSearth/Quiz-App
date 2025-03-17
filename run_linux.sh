#!/bin/bash
# Run script for Quiz App on Linux environments

# Make the script executable
chmod +x run_linux.sh

# Set environment variables
export PYTHONUNBUFFERED=1
export DJANGO_SETTINGS_MODULE=quiz_project.settings

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
fi

# Check for database
if [ ! -f "db.sqlite3" ]; then
    echo "Database not found. Running migrations..."
    python manage.py migrate
fi

# Fix permissions
echo "Fixing permissions..."
if [ -f "db.sqlite3" ]; then
    chmod 664 db.sqlite3
fi

# Create necessary directories
mkdir -p static staticfiles media
chmod -R 755 static staticfiles media

# Check if port 8000 is in use
if netstat -tuln | grep -q ":8000 "; then
    echo "Port 8000 is already in use. Using port 8080 instead."
    PORT=8080
else
    PORT=8000
fi

# Run the server
echo "Starting server on port $PORT..."
python manage.py runserver 0.0.0.0:$PORT 