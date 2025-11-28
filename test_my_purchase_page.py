#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

# Login as u1 and test the actual page
client = Client()
user = User.objects.get(email='u1@gmail.com')

print(f"Testing my-purchase page for user: {user.email}")
print()

# Manually login
client.force_login(user)

# Try different URL formats
urls = ['/my-purchase/', 'my-purchase/', '/my_purchase/', '/my-purchase']
for url in urls:
    try:
        response = client.get(url, follow=True)
        if response.status_code == 200:
            print(f"✓ {url} - Status: {response.status_code}")
            content = response.content.decode('utf-8')
            
            # Check for exam certificates
            if 'Exam Certificates' in content:
                print(f"  → Found 'Exam Certificates' section")
            if 'Download Certificate' in content:
                print(f"  → Found 'Download Certificate' button")
            if 'UI UX Designing' in content:
                print(f"  → Found 'UI UX Designing' course")
            break
    except Exception as e:
        pass

# Print a portion of the page to check
if response.status_code == 200:
    print()
    print("Page content (first 3000 chars):")
    print("-" * 60)
    print(content[:3000])
