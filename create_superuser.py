"""
Script to create a superuser for the Django admin panel
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelance_marketplace.settings')
django.setup()

from django.contrib.auth.models import User

# Use environment variables if available, falling back to defaults
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser created: {username} ({email})')
else:
    print(f'Superuser {username} already exists')
