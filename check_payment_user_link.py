#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from core.models import CoursePayment
from django.contrib.auth.models import User

# Get all successful payments for u1@gmail.com by email
email = 'u1@gmail.com'
payments_by_email = CoursePayment.objects.filter(email=email, status='successful')

print(f"Payments by email '{email}': {payments_by_email.count()}\n")
for p in payments_by_email:
    user_info = f"{p.user.email}" if p.user else "NO USER"
    print(f"  ID {p.id}: {p.course.name}")
    print(f"    Email: {p.email}")
    print(f"    User ID: {p.user_id}")
    print(f"    User: {user_info}")
    print()

# Get the actual user
try:
    user = User.objects.get(email=email)
    print(f"\nUser object found: {user} (ID: {user.id})")
except User.DoesNotExist:
    print(f"\nUser NOT found for email: {email}")

# Now check payments linked by user
print("\n" + "=" * 60)
payments_by_user = CoursePayment.objects.filter(user=user, status='successful')
print(f"Payments by user_id: {payments_by_user.count()}\n")
for p in payments_by_user:
    print(f"  ID {p.id}: {p.course.name}")
    print()
