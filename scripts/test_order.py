"""Test Razorpay order creation."""
import os
import sys
import django
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Course
import json

def main():
    # Create test user if doesn't exist
    username = 'testuser'
    password = 'testpass'
    user = User.objects.filter(username=username).first()
    if not user:
        user = User.objects.create_user(
            username=username,
            email='test@example.com',
            password=password
        )
        print(f"Created test user: {username}")

    # Create test course if doesn't exist
    course = Course.objects.filter(slug='python-test').first()
    if not course:
        course = Course.objects.create(
            name='Python Test Course',
            slug='python-test',
            discounted_price='199.00',
            is_active=True
        )
        print(f"Created test course: {course.name}")

    # Create client and login
    client = Client()
    success = client.login(username=username, password=password)
    print(f"Login successful: {success}")

    # Test order creation
    payload = {
        'first_name': 'Test',
        'last_name': 'User',
        'email': 'test@example.com',
        'phone': '9999999999',
        'address': 'Test Address',
        'city': 'Test City',
        'state': 'Test State',
        'zip': '123456'
    }

    response = client.post(
        f'/course/{course.slug}/create-order/',
        data=json.dumps(payload),
        content_type='application/json'
    )

    print("\nResponse:")
    print(f"Status Code: {response.status_code}")
    print(f"Content: {response.content.decode('utf-8')}")

if __name__ == '__main__':
    main()