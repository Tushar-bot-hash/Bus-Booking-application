from users.models import User
all_users = User.objects.all().values_list('email', 'is_superuser')
print(f"All users: {list(all_users)}")
