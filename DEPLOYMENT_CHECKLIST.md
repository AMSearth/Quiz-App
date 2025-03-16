# Deployment Checklist for Quiz App

Use this checklist to ensure you've completed all necessary steps for deploying the Quiz App to Vercel.

## Pre-Deployment Checklist

- [ ] Code is committed to GitHub repository
- [ ] PostgreSQL database is set up and connection URL is available
- [ ] All required files are created and properly configured:
  - [ ] `vercel.json`
  - [ ] `build_files.sh`
  - [ ] Updated `wsgi.py`
  - [ ] Updated `settings.py`
  - [ ] `.env` (for local development)
  - [ ] `.gitignore`
  - [ ] `requirements.txt`
  - [ ] `vercel_migrate.py` (for database operations)
  - [ ] `backup_db.py` (for database backups)
  - [ ] `restore_db.py` (for database restores)
- [ ] Run `python manage.py check --deploy` to check for deployment issues
- [ ] Test the application locally with PostgreSQL (if possible)
- [ ] Ensure all static files are properly configured
- [ ] Check that all environment variables are documented

## Vercel Deployment Checklist

- [ ] GitHub repository is connected to Vercel
- [ ] Project settings are configured correctly
- [ ] Environment variables are added:
  - [ ] `DEBUG=False`
  - [ ] `SECRET_KEY=your-secure-key`
  - [ ] `DATABASE_URL=your-postgres-url`
- [ ] Initial deployment is successful
- [ ] Vercel CLI is installed
- [ ] Database migrations are applied using `vercel run python vercel_migrate.py migrate`
- [ ] Superuser is created using `vercel run python vercel_migrate.py createsuperuser`
- [ ] Static files are collected using `vercel run python vercel_migrate.py collectstatic`

## Post-Deployment Checklist

- [ ] Test the application on the Vercel URL
- [ ] Check that all pages load correctly
- [ ] Verify that static files (CSS, JS, images) are loading
- [ ] Test user registration and login
- [ ] Test quiz creation and taking
- [ ] Check admin functionality
- [ ] Test on different devices and browsers
- [ ] Monitor for any errors in Vercel logs
- [ ] Create a database backup using `backup_db.py`

## Database Management Checklist

- [ ] Set up a regular backup schedule for your database
- [ ] Test the backup process using `python backup_db.py`
- [ ] Test the restore process using `python restore_db.py`
- [ ] Document the backup and restore procedures for your team
- [ ] Ensure database credentials are stored securely

## Common Issues to Watch For

- [ ] Database connection errors
- [ ] Static files not loading
- [ ] CSRF errors
- [ ] 500 server errors
- [ ] Authentication issues
- [ ] Form submission problems

## Notes

- Remember that Vercel has a serverless architecture, which means there are some limitations compared to traditional hosting.
- The free tier of Vercel has certain limitations on build time and function execution.
- Make sure to regularly backup your database.
- Consider setting up monitoring for your application.

## Resources

- [Vercel Dashboard](https://vercel.com/dashboard)
- [Django Documentation](https://docs.djangoproject.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Detailed Deployment Guide](./DEPLOYMENT_GUIDE.md) 