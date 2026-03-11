#!/bin/sh

python manage.py collectstatic --noinput
python manage.py migrate --noinput

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

email = "$DJANGO_SUPERUSER_EMAIL"
name = "$DJANGO_SUPERUSER_NAME"
password = "$DJANGO_SUPERUSER_PASSWORD"

user, created = User.objects.get_or_create(
    email=email,
    defaults={"name": name}
)

user.set_password(password)
user.is_admin = True
user.is_superuser = True
user.is_active = True
user.save()

print("Admin user ready")
END
exec gunicorn --bind 0.0.0.0:8000 authAPI.wsgi:application
