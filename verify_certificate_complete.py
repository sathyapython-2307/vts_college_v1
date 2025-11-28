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

print(f"Verifying certificate rendering for user: {user.email}\n")

# Manually login
client.force_login(user)

# Get the page
response = client.get('/my-purchase/', follow=True)
content = response.content.decode('utf-8')

# Extract certificate card
pattern = r'<div class="col-12 col-md-6 col-lg-4 mb-3">.*?<div class="card h-100 shadow-sm" style="border-left: 4px solid #28a745;">.*?</div>\s*</div>\s*</div>'
match = re.search(pattern, content, re.DOTALL)

if match:
    card_html = match.group(0)
    print("=" * 80)
    print("EXAM CERTIFICATE CARD HTML:")
    print("=" * 80)
    print(card_html)
    print()
    
    # Check for key elements
    checks = {
        'Certificate card': '<div class="card h-100 shadow-sm"' in card_html,
        'Course name': 'UI UX Designing' in card_html,
        'Score badge': 'badge bg-success' in card_html,
        'Score percentage': '100%' in card_html,
        'Exam date': 'Exam:' in card_html,
        'Score details': 'Score:' in card_html,
        'Duration': 'Duration:' in card_html,
        'Clean attempt': 'Clean attempt' in card_html,
        'Download button': 'btn btn-sm btn-success' in card_html,
        'Download link': '/certificate/' in card_html and '/download/' in card_html,
    }
    
    print("=" * 80)
    print("VERIFICATION CHECKLIST:")
    print("=" * 80)
    for check, result in checks.items():
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {check}")
    
else:
    print("✗ Could not find certificate card in page")
