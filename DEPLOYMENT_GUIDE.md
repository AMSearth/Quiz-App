# Detailed Deployment Guide for Quiz App

This guide provides step-by-step instructions for deploying the Quiz App to Vercel.

## Prerequisites

1. **GitHub Account**: You need a GitHub account to host your code repository.
2. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) using your GitHub account.
3. **PostgreSQL Database**: Vercel doesn't support SQLite in production, so you'll need a PostgreSQL database.
   - Recommended providers: [Supabase](https://supabase.com), [Neon](https://neon.tech), or [Railway](https://railway.app)

## Preparing Your Project

1. **Update your code for production**:
   - Ensure all necessary files are created:
     - `vercel.json`: Configuration for Vercel deployment
     - `build_files.sh`: Build script for static files and migrations
     - Updated `wsgi.py`: With Vercel handler
     - Updated `settings.py`: With production settings
     - `.env`: For local development
     - `.gitignore`: To exclude sensitive files
     - `requirements.txt`: With all dependencies

2. **Test locally**:
   ```bash
   python manage.py check --deploy
   ```
   This will check for common deployment issues.

## Setting Up PostgreSQL Database

1. **Create a PostgreSQL database** with one of the recommended providers.
2. **Get your database connection URL** in the format:
   ```
   postgres://username:password@host:port/database_name
   ```
3. **Test the connection** locally by adding the URL to your `.env` file and running:
   ```bash
   python manage.py migrate
   ```

## Deploying to GitHub

1. **Initialize Git** (if not already done):
   ```bash
   git init
   ```

2. **Add your files**:
   ```bash
   git add .
   ```

3. **Commit your changes**:
   ```bash
   git commit -m "Initial commit for Vercel deployment"
   ```

4. **Create a new repository** on GitHub.

5. **Link and push to your repository**:
   ```bash
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git branch -M main
   git push -u origin main
   ```

## Deploying to Vercel

1. **Log in to Vercel** and go to your dashboard.

2. **Import your project**:
   - Click "Add New" > "Project"
   - Select your GitHub repository
   - Vercel will automatically detect Django

3. **Configure project settings**:
   - Framework Preset: Other (or Django if available)
   - Build Command: Leave empty (handled by vercel.json)
   - Output Directory: Leave empty
   - Install Command: Leave empty

4. **Add environment variables**:
   - `DEBUG`: `False`
   - `SECRET_KEY`: Generate a secure key (you can use [Djecrety](https://djecrety.ir/))
   - `DATABASE_URL`: Your PostgreSQL connection URL
   - Any other environment variables your app needs

5. **Deploy**:
   - Click "Deploy"
   - Vercel will build and deploy your application

## Post-Deployment Steps

1. **Install Vercel CLI**:
   ```bash
   npm i -g vercel
   ```

2. **Login to Vercel CLI**:
   ```bash
   vercel login
   ```

3. **Run migrations using the Vercel migration script**:
   ```bash
   vercel run python vercel_migrate.py migrate
   ```

4. **Create a superuser using the Vercel migration script**:
   ```bash
   vercel run python vercel_migrate.py createsuperuser --username admin --email admin@example.com
   ```
   You'll be prompted to enter a password, or you can provide it with the `--password` option.

5. **Collect static files if needed**:
   ```bash
   vercel run python vercel_migrate.py collectstatic
   ```

## Using the Vercel Migration Script

The project includes a `vercel_migrate.py` script that simplifies common tasks when working with Vercel:

### Running Migrations

```bash
vercel run python vercel_migrate.py migrate
```

### Creating a Superuser

```bash
vercel run python vercel_migrate.py createsuperuser --username admin --email admin@example.com --password securepassword
```

If you omit the `--password` option, you'll be prompted to enter it interactively.

### Collecting Static Files

```bash
vercel run python vercel_migrate.py collectstatic
```

## Database Management

The project includes scripts for backing up and restoring your PostgreSQL database:

### Creating a Backup

```bash
python backup_db.py --dir ./backups
```

This will create a backup of your database in the specified directory.

### Restoring from a Backup

```bash
python restore_db.py path/to/backup_file.sql
```

This will restore your database from the specified backup file.

## Troubleshooting

### Common Issues

1. **Database Connection Errors**:
   - Check if your `DATABASE_URL` is correct
   - Ensure your database provider allows connections from Vercel's IP addresses

2. **Static Files Not Loading**:
   - Verify that `STATIC_ROOT` and `STATICFILES_STORAGE` are correctly set
   - Make sure WhiteNoise middleware is included

3. **500 Server Errors**:
   - Check Vercel logs for detailed error messages
   - Temporarily set `DEBUG=True` to see error details (remember to set it back to `False`)

4. **CSRF Errors**:
   - Ensure your Vercel domain is included in `CSRF_TRUSTED_ORIGINS`

### Viewing Logs

To view deployment logs:
1. Go to your project on Vercel dashboard
2. Click on the latest deployment
3. Click "View Logs"

## Updating Your Application

To update your application after making changes:

1. **Commit and push changes** to GitHub:
   ```bash
   git add .
   git commit -m "Update description"
   git push
   ```

2. **Vercel will automatically deploy** the new changes if you have auto-deployment enabled.

3. **Run migrations** if you've made database changes:
   ```bash
   vercel run python vercel_migrate.py migrate
   ```

## Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Django Documentation](https://docs.djangoproject.com/en/4.2/howto/deployment/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/en/stable/)
- [dj-database-url Documentation](https://github.com/jazzband/dj-database-url) 