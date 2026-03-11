#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate --noinput

# Create superuser only if it doesn't exist
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

name = "$DJANGO_SUPERUSER_NAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"

if not User.objects.filter(name=name).exists():
    print("Creating admin user...")
    User.objects.create_superuser(name, email, password)
else:
    print("Admin user already exists.")
END

exec gunicorn --bind 0.0.0.0:8000 authAPI.wsgi:application
