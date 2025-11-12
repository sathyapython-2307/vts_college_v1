import os
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth.models import User
from core.models import Course

# Create test user
username = 'testuser'
password = 'testpass'
if not User.objects.filter(username=username).exists():
    User.objects.create_user(username=username, email='test@example.com', password=password)

# Create a test course
slug = 'python-fullstack'
if not Course.objects.filter(slug=slug).exists():
    Course.objects.create(name='Python Fullstack Test', discounted_price='199.00', slug=slug, is_active=True)

# Use Django test client to simulate logged-in user
c = Client()
logged = c.login(username=username, password=password)
print('logged_in', logged)

payload = {
    'first_name': 'Alice',
    'last_name': 'Smith',
    'email': 'alice@example.com',
    'phone': '9999999999',
    'address': '123 Test St',
    'city': 'Testville',
    'state': 'TS',
    'zip': '12345'
}

resp = c.post(f'/course/{slug}/create-order/', data=json.dumps(payload), content_type='application/json')
print('STATUS', resp.status_code)
print(resp.content.decode('utf-8'))
