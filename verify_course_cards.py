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
print("CHECKING COURSE CARDS FOR u1@gmail.com")
print("=" * 80)

courses = ['Python Full Stack', 'Java Full Stack', 'UI/UX Design']

print("\nCourse Card Images:")
for course in courses:
    found = course in content
    symbol = "✓" if found else "✗"
    print(f"  {symbol} {course}")

# Extract all course card images
pattern = r'<img src="([^"]*course_purchase_cards[^"]*)" class="course-image"'
images = re.findall(pattern, content)

print(f"\nCourse card images found: {len(images)}")
for i, img_url in enumerate(images, 1):
    print(f"  {i}. {img_url}")

# Extract all course titles
pattern = r'<h3 class="course-title">([^<]+)</h3>'
titles = re.findall(pattern, content)

print(f"\nCourse titles found: {len(titles)}")
for i, title in enumerate(titles, 1):
    print(f"  {i}. {title}")
