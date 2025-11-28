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

# Look for progress bar percentage
progress_pattern = r'style="width:\s*(\d+(?:\.\d+)?(?:px|%)?);"'
matches = re.findall(progress_pattern, content)

print("Progress bar widths found:")
for i, width in enumerate(matches):
    print(f"  {i+1}. {width}")

# Look for specific progress data
if 'style="width: 0%' in content:
    print("\n⚠️  Progress bar showing 0% - course not started")
elif 'style="width: 100%' in content:
    print("\n✓ Progress bar showing 100% - course completed!")
else:
    print("\n✓ Progress bar showing progress")

# Check progress value from template rendering
prog_match = re.search(r'progress-bar.*?style="width:\s*([^"]+)"', content, re.DOTALL)
if prog_match:
    print(f"Progress value: {prog_match.group(1)}")
