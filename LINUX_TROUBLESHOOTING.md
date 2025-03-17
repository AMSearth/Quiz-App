# Linux Troubleshooting Guide for Quiz App

This guide addresses common issues when running the Quiz App on Linux environments.

## Common Issues and Solutions

### 1. ValueError when Running Server

If you're experiencing a ValueError when running `python manage.py runserver` on Linux, it's likely due to one of these issues:

#### Missing View Functions

The error logs show that there might be URL patterns referencing view functions that don't exist:

```
AttributeError: module 'quiz_app.views' has no attribute 'delete_quiz'. Did you mean: 'create_quiz'?
```

**Solution:**
- Make sure you've pulled the latest code from GitHub which includes all view functions
- Run `git pull` to get the latest changes
- Check that `quiz_app/views.py` contains all the required view functions

#### File Permission Issues

Linux has stricter file permissions than Windows:

**Solution:**
- Run the following commands to fix permissions:
  ```bash
  chmod 664 db.sqlite3
  chmod -R 755 static staticfiles media
  ```

#### Socket Binding Issues

On Linux, binding to port 8000 might require elevated privileges:

**Solution:**
- Try using a higher port number:
  ```bash
  python manage.py runserver 8080
  ```
- Or bind to all interfaces:
  ```bash
  python manage.py runserver 0.0.0.0:8000
  ```

### 2. Database Migration Issues

If you're having issues with database migrations:

**Solution:**
- Reset migrations (if needed):
  ```bash
  find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
  find . -path "*/migrations/*.pyc" -delete
  rm db.sqlite3
  python manage.py makemigrations
  python manage.py migrate
  ```

### 3. Static Files Not Loading

If static files aren't loading properly:

**Solution:**
- Collect static files:
  ```bash
  python manage.py collectstatic --noinput
  ```
- Check permissions:
  ```bash
  chmod -R 755 static staticfiles
  ```

## Quick Setup Script

For a quick setup on Linux, run:

```bash
# Make the script executable
chmod +x run_linux.sh

# Run the script
./run_linux.sh
```

## Manual Setup Steps

If you prefer to set up manually:

1. **Fix permissions**:
   ```bash
   chmod 664 db.sqlite3
   chmod -R 755 static staticfiles media
   mkdir -p static staticfiles media
   ```

2. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Create superuser** (if needed):
   ```bash
   python manage.py createsuperuser
   ```

4. **Fix superuser profiles**:
   ```bash
   python fix_superuser.py
   ```

5. **Run server with proper binding**:
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Environment Setup

Make sure you have the correct Python packages installed:

```bash
pip install -r requirements.txt
```

## Debugging

For detailed debugging information:

```bash
# Run with verbose output
python manage.py runserver --verbosity 2

# Check for specific errors
python manage.py check

# Test the UserProfile model
python test_model.py
``` 