python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

name = "$DJANGO_SUPERUSER_NAME"
email = "$DJANGO_SUPERUSER_EMAIL"
password = "$DJANGO_SUPERUSER_PASSWORD"

user, created = User.objects.get_or_create(
    email=email,
    defaults={"name": name}
)

if created:
    print("Creating admin user...")
    user.set_password(password)

# force admin permissions
user.is_admin = True
user.is_staff = True
user.is_superuser = True
user.is_active = True

user.save()
print("Admin user ready.")
END
