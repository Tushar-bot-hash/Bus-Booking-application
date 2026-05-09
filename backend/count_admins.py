import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bus_booking.settings')
django.setup()

from users.models import User

admin_count = User.objects.filter(is_superuser=True).count()
admin_users = User.objects.filter(is_superuser=True).values_list('email', flat=True)

print(f"Total admin users: {admin_count}")
print(f"Admin emails: {list(admin_users)}")
