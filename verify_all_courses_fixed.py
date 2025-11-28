#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
import re

# Login and get the page
client = Client()
user = User.objects.get(email='u1@gmail.com')
client.force_login(user)

response = client.get('/my-purchase/', follow=True)
content = response.content.decode('utf-8')

print("=" * 80)
print("CHECKING ALL COURSES FOR u1@gmail.com")
print("=" * 80)

courses_to_check = [
    'UI/UX Design',
    'UI UX Designing',
    'Java Full Stack',
    'Python Full Stack',
]

print("\nCourse Presence:")
for course in courses_to_check:
    found = course in content
    symbol = "✓" if found else "✗"
    print(f"  {symbol} {course}")

# Count course cards
course_cards = content.count('course-card')
print(f"\nTotal course cards in HTML: {course_cards}")

# Extract course titles
pattern = r'<h3 class="course-title">([^<]+)</h3>'
matches = re.findall(pattern, content)
print(f"\nFound course titles:")
for i, title in enumerate(matches, 1):
    print(f"  {i}. {title}")

# Count start learning buttons
start_buttons = content.count('Start Learning') + content.count('Continue Learning')
print(f"\nTotal Start/Continue Learning buttons: {start_buttons}")
