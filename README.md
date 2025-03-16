# Quiz App

Version: 1.0.0

An interactive platform for creating and taking quizzes online. Perfect for teachers, students, and educational institutions.

## Features

- User registration and approval system
- Teacher dashboard for creating and managing quizzes
- Student dashboard for taking quizzes
- Real-time quiz taking with timer
- Detailed quiz results and statistics
- Admin panel for user management
- Light/Dark theme toggle

## Local Development

### Quick Setup

The easiest way to set up the project is to use the included setup script:

```bash
python setup_local.py
```

This will:
1. Create a virtual environment
2. Install dependencies
3. Create a `.env` file with a random secret key
4. Run migrations
5. Create a superuser
6. Collect static files
7. Optionally start the development server

### Manual Setup

If you prefer to set up manually:

1. Clone the repository
2. Create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env` file
5. Run migrations:
   ```
   python manage.py migrate
   ```
6. Create a superuser:
   ```
   python manage.py createsuperuser
   ```
7. Run the development server:
   ```
   python manage.py runserver
   ```

## Deployment on Vercel

### Prerequisites

1. A GitHub account
2. A Vercel account (sign up at vercel.com using your GitHub account)
3. A PostgreSQL database (You can use Supabase, Neon, or any other PostgreSQL provider)

### Steps to Deploy

1. Push your code to a GitHub repository

2. Set up a PostgreSQL database and get the connection URL

3. Connect your GitHub repository to Vercel:
   - Go to [Vercel Dashboard](https://vercel.com/dashboard)
   - Click "Add New" > "Project"
   - Select your GitHub repository
   - Configure the project:
     - Framework Preset: Other
     - Build Command: Leave empty (handled by vercel.json)
     - Output Directory: Leave empty
     - Install Command: Leave empty

4. Add environment variables in Vercel:
   - `DEBUG`: False
   - `SECRET_KEY`: Your secure secret key
   - `DATABASE_URL`: Your PostgreSQL connection URL

5. Deploy the project

6. After deployment, run migrations:
   - Install Vercel CLI: `npm i -g vercel`
   - Login to Vercel: `vercel login`
   - Run migrations: `vercel run python vercel_migrate.py migrate`

7. Create a superuser:
   - `vercel run python vercel_migrate.py createsuperuser --username admin --email admin@example.com`

## Database Management

### Backup

The application includes a script for backing up your PostgreSQL database:

```bash
python backup_db.py --dir ./backups
```

Options:
- `--dir`, `-d`: Directory to store the backup (default: ./backups)
- `--url`, `-u`: Database URL (default: read from DATABASE_URL env var)

### Restore

To restore a database from a backup:

```bash
python restore_db.py path/to/backup_file.sql
```

Options:
- `--url`, `-u`: Database URL (default: read from DATABASE_URL env var)

## Utility Scripts

The project includes several utility scripts to help with development and deployment:

### Local Development

- `setup_local.py`: Sets up the local development environment
  ```bash
  python setup_local.py [command]
  ```
  Available commands:
  - `setup`: Run all setup steps (default)
  - `venv`: Create a virtual environment
  - `install`: Install requirements
  - `env`: Create .env file
  - `migrate`: Run migrations
  - `createsuperuser`: Create a superuser
  - `collectstatic`: Collect static files
  - `runserver`: Run the development server

### Vercel Deployment

- `vercel_migrate.py`: Helps with database operations on Vercel
  ```bash
  vercel run python vercel_migrate.py [command]
  ```
  Available commands:
  - `migrate`: Run migrations
  - `createsuperuser`: Create a superuser
  - `collectstatic`: Collect static files

### Release Management

- `create_release.py`: Helps with creating a new release
  ```bash
  python create_release.py [version_type] [options]
  ```
  Version types:
  - `major`: Increment major version (x.0.0)
  - `minor`: Increment minor version (0.x.0)
  - `patch`: Increment patch version (0.0.x)
  
  Options:
  - `--message`, `-m`: Release message
  - `--no-tag`: Do not tag the release
  
  This script will:
  1. Update the version number in VERSION file and README.md
  2. Create or update CHANGELOG.md with changes since the last tag
  3. Create a git tag for the release

## Documentation

For more detailed information, see the following documents:
- [Deployment Guide](./DEPLOYMENT_GUIDE.md)
- [Deployment Checklist](./DEPLOYMENT_CHECKLIST.md)
- [Changelog](./CHANGELOG.md)

## License

Created by Ajinkya Shinde 