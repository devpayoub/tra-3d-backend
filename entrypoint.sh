#!/bin/sh

# Collect static files (required for Admin panel with DEBUG=False)
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Create superuser automatically if it doesn't exist
python manage.py createsuperuser \
    --noinput \
    --name $DJANGO_SUPERUSER_NAME \
    --email $DJANGO_SUPERUSER_EMAIL || true

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 authAPI.wsgi:application
