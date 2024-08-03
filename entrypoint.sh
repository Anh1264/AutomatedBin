#!/bin/bash
until nc -z ep-red-union-a5suo4nb.us-east-2.aws.neon.tech 5432; do
  echo "Waiting for database connection..."
  sleep 1
done

# Apply database migrations (only for Django service)
python manage.py migrate --noinput
# python manage.py collectstatic --no-input --clear

# Start the Django/Gunicorn server using Railway's $PORT
gunicorn myproject.wsgi:application --bind 0.0.0.0:$PORT &

# gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 &
tail -f /dev/null
