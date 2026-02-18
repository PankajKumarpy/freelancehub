"""
Script to create a superuser for the Django admin panel
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'freelance_marketplace.settings')
django.setup()

from django.contrib.auth.models import User

# Create superuser
username = 'admin'
email = 'admin@example.com'
password = 'admin123'

if User.objects.filter(username=username).exists():
    print(f'Superuser "{username}" already exists!')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'Superuser created successfully!')
    print(f'Username: {username}')
    print(f'Password: {password}')
    print(f'Email: {email}')
    print(f'\nYou can now login at: http://127.0.0.1:8000/admin/')
