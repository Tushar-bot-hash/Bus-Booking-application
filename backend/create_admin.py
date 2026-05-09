import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_booking.settings')
django.setup()

from users.models import User

email = 'admin@example.com'
password = 'adminpassword123'
first_name = 'Admin'
last_name = 'User'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email=email, password=password, first_name=first_name, last_name=last_name)
    print(f"Superuser {email} created successfully.")
else:
    print(f"Superuser {email} already exists.")
