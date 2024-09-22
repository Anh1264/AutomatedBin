#!/bin/bash

# 1. Database Connection Check (with error handling and logging)
echo "Waiting for database connection..."
until nc -z ep-red-union-a5suo4nb.us-east-2.aws.neon.tech 5432; do
    sleep 1
done
echo "Database connection established!"

# 2. Apply database migrations (only for Django service)
echo "Applying database migrations..."
python manage.py migrate --noinput
echo "Migrations applied successfully!"

# 3. Start the Django/Gunicorn server 
echo "Starting Gunicorn server..."
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT &
echo "Gunicorn server started in the background!"

# 4. Start Celery worker (if applicable)
# Uncomment and adjust the following lines if you're using Celery
# echo "Starting Celery worker..."
# celery -A myproject worker -l info &  # Replace 'myproject' with your actual project name
# echo "Celery worker started in the background!"

# 5. Keep the Container Running 
tail -f /dev/null