#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

# Login and check the page
client = Client()
user = User.objects.get(email='u1@gmail.com')
client.force_login(user)

response = client.get('/my-purchase/', follow=True)
content = response.content.decode('utf-8')

# Look for course card section
import re

# Find the courses tab section
pattern = r'id="courses".*?<div class="alert alert-info text-center'
match = re.search(pattern, content, re.DOTALL)

if match:
    courses_section = match.group(0)
    # Check for course cards
    if 'course-card' in courses_section:
        print("✓ Course cards found in Courses tab")
        
        # Count course cards
        card_count = courses_section.count('course-card')
        print(f"  Number of course cards: {card_count}")
        
        # Show first part
        print("\nFirst 2000 chars of Courses section:")
        print("-" * 60)
        print(courses_section[:2000])
    else:
        print("✗ No course cards found")
        print("\nFirst 2000 chars of Courses section:")
        print("-" * 60)
        print(courses_section[:2000])
else:
    print("Could not find courses tab")
    
# Also check for course names
if 'UI UX Designing' in content:
    print("\n✓ 'UI UX Designing' course name found in page")
else:
    print("\n✗ 'UI UX Designing' course name NOT found in page")
