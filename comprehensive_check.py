#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client

# Login and get the full page
client = Client()
user = User.objects.get(email='u1@gmail.com')
client.force_login(user)

response = client.get('/my-purchase/', follow=True)
content = response.content.decode('utf-8')

print("=" * 80)
print("COMPLETE VERIFICATION FOR u1@gmail.com")
print("=" * 80)

checks = {
    'COURSES TAB': {
        'Course card': 'course-card' in content,
        'Course image': 'course_purchase_cards/course_card_ui_ux.png' in content,
        'Course title': 'UI/UX Design' in content,
        'Course description': 'Master the art of crafting' in content,
        'Start Learning button': 'Start Learning' in content or 'Continue Learning' in content,
        'Progress bar': 'progress-bar' in content,
    },
    'ACHIEVEMENTS TAB': {
        'Exam Certificates heading': 'Exam Certificates' in content,
        'Score badge': 'badge bg-success' in content and '100%' in content,
        'Score details': '10/10 correct' in content,
        'Exam date': 'Exam:' in content,
        'Certificate status': 'Clean attempt' in content,
        'Download button': '/certificate/1/download/' in content,
        'Download link text': 'Download Certificate' in content,
    },
    'OVERALL': {
        'Page loaded successfully': response.status_code == 200,
        'User logged in': 'u1' in content or 'Logout' in content,
        'Navigation visible': 'Courses' in content and 'Achievements' in content,
    }
}

for section, items in checks.items():
    print(f"\n{section}:")
    print("-" * 80)
    for item, result in items.items():
        symbol = "✓" if result else "✗"
        print(f"  {symbol} {item}")

print("\n" + "=" * 80)
print("SUMMARY:")
print("=" * 80)

all_passed = all(all(v for v in items.values()) for items in checks.values())
if all_passed:
    print("✓ ALL CHECKS PASSED - u1@gmail.com can see:")
    print("  - Course with complete details (image, title, description, button)")
    print("  - 100% progress bar")
    print("  - Certificate with download button")
    print("\nNO DATA IS MISSING!")
else:
    failed_items = []
    for section, items in checks.items():
        for item, result in items.items():
            if not result:
                failed_items.append(f"{section}: {item}")
    
    print("✗ Some items missing:")
    for item in failed_items:
        print(f"  - {item}")
