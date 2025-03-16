#!/bin/bash
# Build script for Vercel deployment

echo "Starting build process..."

# Create necessary directories
mkdir -p static staticfiles

# Install dependencies
pip install -r requirements.txt

# Run setup script
python vercel_setup.py

# Collect static files
python manage.py collectstatic --noinput

echo "Build process completed!" 