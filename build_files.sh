#!/bin/bash
# Build script for Vercel deployment

# Make the file executable
chmod a+x build_files.sh

# Install dependencies
python3 -m pip install -r requirements.txt

# Collect static files
python3 manage.py collectstatic --noinput

# Apply migrations
python3 manage.py migrate 