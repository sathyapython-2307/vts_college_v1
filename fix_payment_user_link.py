#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from core.models import CoursePayment, CourseAccess
from django.contrib.auth.models import User

# Get the correct user
u1 = User.objects.get(email='u1@gmail.com')
print(f"Target User: {u1.email} (ID: {u1.id})\n")

# Get all payments with u1@gmail.com email but wrong user_id
wrong_user_payments = CoursePayment.objects.filter(email='u1@gmail.com', status='successful').exclude(user=u1)
print(f"Payments with wrong user_id: {wrong_user_payments.count()}\n")

for payment in wrong_user_payments:
    old_user = payment.user
    print(f"Payment ID {payment.id}: {payment.course.name}")
    print(f"  Current user: {old_user.email} (ID: {old_user.id})")
    print(f"  Fixing to: {u1.email} (ID: {u1.id})")
    
    # Update the user
    payment.user = u1
    payment.save()
    
    # Now create CourseAccess if it doesn't exist
    access, created = CourseAccess.objects.get_or_create(
        user=u1,
        course=payment.course,
        defaults={
            'payment': payment,
            'is_active': True
        }
    )
    
    if created:
        print(f"  ✓ Created CourseAccess (ID: {access.id})")
    else:
        # Update existing if payment is not set
        if not access.payment:
            access.payment = payment
            access.save()
        print(f"  ✓ CourseAccess exists (ID: {access.id})")
    
    print()

print("=" * 60)
print("Final CourseAccess for u1@gmail.com:")
accesses = CourseAccess.objects.filter(user=u1, is_active=True).order_by('created_at')
for access in accesses:
    print(f"  - {access.course.name} (Access ID: {access.id})")
