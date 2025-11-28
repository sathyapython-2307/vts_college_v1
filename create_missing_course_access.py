#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import CoursePayment, CourseAccess

user = User.objects.get(email='u1@gmail.com')

print(f"Processing CoursePayment records for {user.email}\n")

# Get all successful payments for this user
payments = CoursePayment.objects.filter(user=user, status='successful').order_by('created_at')
print(f"Successful Payments: {payments.count()}\n")

created_count = 0
for payment in payments:
    print(f"Payment ID: {payment.id}")
    print(f"  Course: {payment.course.name}")
    
    # Try to get existing access
    existing = CourseAccess.objects.filter(user=user, course=payment.course).first()
    
    if existing:
        print(f"  Status: ✓ CourseAccess already exists (ID: {existing.id})")
        # Update the payment link if not set
        if not existing.payment:
            existing.payment = payment
            existing.save()
            print(f"  Updated: Linked payment {payment.id}")
    else:
        # Create new CourseAccess
        try:
            access = CourseAccess.objects.create(
                user=user,
                course=payment.course,
                payment=payment,
                is_active=True
            )
            print(f"  Status: ✓ Created new CourseAccess (ID: {access.id})")
            created_count += 1
        except Exception as e:
            print(f"  Status: ✗ Error creating CourseAccess: {e}")
    
    print()

print("=" * 60)
print(f"Summary: Created {created_count} new CourseAccess records")

# Verify
print("\nFinal CourseAccess records for u1@gmail.com:")
accesses = CourseAccess.objects.filter(user=user, is_active=True)
for access in accesses:
    print(f"  - {access.course.name} (Access ID: {access.id}, Payment: {access.payment_id})")
