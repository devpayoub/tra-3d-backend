#!/bin/sh

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Apply migrations
echo "Applying migrations..."
python manage.py migrate --noinput

# Create superuser safely if it doesn't exist
echo "Checking for admin user..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

email = "$DJANGO_SUPERUSER_EMAIL"
name = "$DJANGO_SUPERUSER_NAME"
password = "$DJANGO_SUPERUSER_PASSWORD"

if not User.objects.filter(email=email).exists():
    print("Creating admin user...")
    User.objects.create_superuser(email=email, name=name, password=password)
else:
    print("Admin user already exists.")
END

# Start Gunicorn server
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:8000 authAPI.wsgi:application
