#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from core.models import Course, CoursePurchaseCard
from django.core.exceptions import ObjectDoesNotExist

# Get all courses
courses = Course.objects.all().order_by('name')

print("=" * 80)
print("COURSE PURCHASE CARDS STATUS")
print("=" * 80)

for course in courses:
    print(f"\nCourse: {course.name}")
    print(f"  Slug: {course.slug}")
    
    # Check purchase card
    try:
        card = course.purchase_card
        print(f"  ✓ Purchase Card exists (ID: {card.id})")
        print(f"    Title: {card.title}")
        print(f"    Card Image: {card.card_image if card.card_image else '✗ NO IMAGE'}")
        if card.card_image:
            print(f"    Image URL: {card.card_image.url}")
    except ObjectDoesNotExist:
        print(f"  ✗ NO Purchase Card")
