#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
import re

# Login as u1 and test the actual page
client = Client()
user = User.objects.get(email='u1@gmail.com')

print(f"Testing my-purchase page for user: {user.email}")
print()

# Manually login
client.force_login(user)

# Get the page
response = client.get('/my-purchase/', follow=True)
content = response.content.decode('utf-8')

# Extract just the achievements tab section
pattern = r'id="achievements".*?<div class="alert alert-info text-center'
match = re.search(pattern, content, re.DOTALL)

if match:
    achievements_section = match.group(0)
    print("=" * 80)
    print("ACHIEVEMENTS TAB SECTION:")
    print("=" * 80)
    print(achievements_section[:4000])
    if len(achievements_section) > 4000:
        print(f"\n... (truncated, total length: {len(achievements_section)})")
else:
    print("Could not find achievements section")
    
# Also search for download link
if '/certificate/' in content and '/download/' in content:
    # Find the link
    cert_link_pattern = r'href="(/certificate/\d+/download/)"'
    cert_links = re.findall(cert_link_pattern, content)
    print()
    print("=" * 80)
    print(f"FOUND CERTIFICATE DOWNLOAD LINKS: {len(cert_links)}")
    print("=" * 80)
    for link in cert_links:
        print(f"  {link}")
