#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import CourseAccess

user = User.objects.get(email='u1@gmail.com')
accesses = CourseAccess.objects.filter(user=user, is_active=True)

print(f"User: {user.email}")
print(f"Active Course Accesses: {accesses.count()}\n")

for access in accesses:
    print(f"Course Access ID: {access.id}")
    print(f"  Course: {access.course}")
    print(f"  Course Name: {access.course.name}")
    print(f"  Course Description: {access.course.description[:100] if access.course.description else 'NO DESC'}")
    print(f"  Course Slug: {access.course.slug}")
    print()
    print(f"  Purchase Card: {access.course.purchase_card}")
    if access.course.purchase_card:
        print(f"    - Title: {access.course.purchase_card.title}")
        print(f"    - Description: {access.course.purchase_card.description[:100]}")
        print(f"    - Card Image: {access.course.purchase_card.card_image}")
    print()
    print(f"  Browser Image: {access.course.browser_image}")
    print()
    print(f"  Progress: {access.progress}")
    print()
