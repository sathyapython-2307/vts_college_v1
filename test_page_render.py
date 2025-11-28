#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory, Client
from core.views import my_purchase
import re

# Login as u1 and test the actual page
client = Client()
user = User.objects.get(email='u1@gmail.com')

print(f"Testing /my-purchase/ for user: {user.email}")
print()

# Manually login
client.force_login(user)

# Get the page
response = client.get('/my-purchase/')

print(f"Response status: {response.status_code}")
print()

# Check if page content mentions exam certificates
content = response.content.decode('utf-8')

# Look for specific markers
print("Checking template rendering:")
if 'Achievements & Certificates' in content:
    print("✓ Found 'Achievements & Certificates' heading")
else:
    print("✗ NOT found 'Achievements & Certificates' heading")

if 'Exam Certificates' in content:
    print("✓ Found 'Exam Certificates' section")
else:
    print("✗ NOT found 'Exam Certificates' section")

if 'Download Certificate' in content:
    print("✓ Found 'Download Certificate' button")
else:
    print("✗ NOT found 'Download Certificate' button")

if 'Certificate pending upload' in content:
    print("✓ Found 'Certificate pending upload' message")
else:
    print("✗ NOT found 'Certificate pending upload' message")

if 'UI UX Designing' in content:
    print("✓ Found 'UI UX Designing' course name")
else:
    print("✗ NOT found 'UI UX Designing' course name")

print()
print("=" * 60)
print("Looking for exam certificate mentions in HTML:")
print("=" * 60)

# Extract the achievements tab content
pattern = r'<div class="tab-pane fade[^>]*id="achievements"[^>]*>.*?</div>\s*</div>\s*</div>'
match = re.search(pattern, content, re.DOTALL)

if match:
    achievements_content = match.group(0)
    # Show first 2000 chars
    print(achievements_content[:2000])
    if len(achievements_content) > 2000:
        print(f"\n... (truncated, total length: {len(achievements_content)})")
else:
    print("Could not extract achievements tab content")
