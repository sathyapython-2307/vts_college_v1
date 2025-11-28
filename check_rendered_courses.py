#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
import re

# Login and check the page
client = Client()
user = User.objects.get(email='u1@gmail.com')
client.force_login(user)

response = client.get('/my-purchase/', follow=True)
content = response.content.decode('utf-8')

# Look for course card in the HTML
if 'course-card' in content:
    print("✓ Course card class found in HTML")
else:
    print("✗ No course-card class found")

# Look for course title
if 'UI/UX Design' in content or 'UI UX Designing' in content:
    print("✓ Course title found")
else:
    print("✗ Course title not found")

# Look for course description
if 'Master the art of crafting' in content or 'user-friendly digital' in content:
    print("✓ Course description found")
else:
    print("✗ Course description not found")

# Look for Start Learning button
if 'Start Learning' in content:
    print("✓ Start Learning button found")
else:
    print("✗ Start Learning button not found")

# Look for course image
if 'course_purchase_cards' in content:
    print("✓ Course purchase card image found")
    # Extract the image URL
    img_match = re.search(r'src="(/media/course_purchase_cards/[^"]+)"', content)
    if img_match:
        print(f"  Image URL: {img_match.group(1)}")
else:
    print("✗ No course purchase card image")

# Look for progress bar
if 'progress-bar' in content:
    print("✓ Progress bar found")
else:
    print("✗ Progress bar not found")

# Extract and show the course card section
print("\n" + "=" * 80)
print("COURSE CARD HTML SECTION:")
print("=" * 80)
pattern = r'<div class="col-12 col-md-6 col-lg-4">.*?<div class="course-card">.*?</div>\s*</div>\s*</div>'
match = re.search(pattern, content, re.DOTALL)
if match:
    card_html = match.group(0)
    print(card_html[:1500])
    if len(card_html) > 1500:
        print(f"\n... (truncated, total length: {len(card_html)})")
else:
    print("Could not extract course card HTML")
