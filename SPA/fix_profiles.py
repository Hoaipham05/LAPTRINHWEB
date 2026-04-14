#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SPA.settings')
django.setup()

from django.contrib.auth.models import User
from accounts.models import UserProfile

# Xóa user admin nếu tồn tại
try:
    User.objects.get(email='admin@maitramspa.com').delete()
    print("Deleted old admin user")
except:
    pass

# Xóa tất cả profiles
UserProfile.objects.all().delete()
print("Deleted all profiles")

# Tạo lại profiles cho user hiện tại
for user in User.objects.all():
    profile, created = UserProfile.objects.get_or_create(user=user, defaults={'role': 'customer'})
    if created:
        print(f"Created profile for {user.email}")
    else:
        print(f"Profile already exists for {user.email}")

# Update nhanvien profile to staff
nhanvien = User.objects.get(email='nhanvien@maitramspa.com')
nhanvien.profile.role = 'staff'
nhanvien.profile.save()
print(f"Updated {nhanvien.email} to staff role")

