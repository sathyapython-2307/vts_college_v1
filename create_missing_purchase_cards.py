#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from core.models import Course, CoursePurchaseCard

# Get the courses that need purchase cards
python_course = Course.objects.get(slug='python-fullstack')
java_course = Course.objects.get(slug='java-fullstack')

print("Creating purchase cards for missing courses...\n")

# Python Full Stack - use course_card_python.png
python_card, created = CoursePurchaseCard.objects.get_or_create(
    course=python_course,
    defaults={
        'title': 'Python Full Stack',
        'description': 'Master Python, Django, and modern web development. Learn backend and frontend technologies to become a full-stack developer.',
        'card_image': 'course_purchase_cards/course_card_python.png',
        'button_text': 'Start Learning'
    }
)

if created:
    print(f"✓ Created CoursePurchaseCard for Python Full Stack")
    print(f"  ID: {python_card.id}")
    print(f"  Image: {python_card.card_image}")
else:
    print(f"✓ Python Full Stack purchase card already exists")
    print(f"  ID: {python_card.id}")

print()

# Java Full Stack - use course_card_python.png (same image for now)
java_card, created = CoursePurchaseCard.objects.get_or_create(
    course=java_course,
    defaults={
        'title': 'Java Full Stack',
        'description': 'Learn Java, Spring Boot, and modern web development. Build scalable enterprise applications with the Java Full Stack.',
        'card_image': 'course_purchase_cards/course_card_python.png',
        'button_text': 'Start Learning'
    }
)

if created:
    print(f"✓ Created CoursePurchaseCard for Java Full Stack")
    print(f"  ID: {java_card.id}")
    print(f"  Image: {java_card.card_image}")
else:
    print(f"✓ Java Full Stack purchase card already exists")
    print(f"  ID: {java_card.id}")

print("\n" + "=" * 60)
print("Purchase cards created successfully!")
print("\nCourse purchase card status:")
for course in [python_course, java_course]:
    try:
        card = course.purchase_card
        print(f"  ✓ {course.name}: {card.card_image}")
    except:
        print(f"  ✗ {course.name}: NO CARD")
