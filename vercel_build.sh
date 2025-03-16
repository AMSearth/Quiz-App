#!/bin/bash

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Collecting static files..."
python -m django collectstatic --noinput

echo "Build completed!" 