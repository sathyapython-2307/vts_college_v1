import os
import json
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from core.models import Course

def main():
    # Create test user if needed
    username = 'testuser5'
    password = 'testpass5'
    if not User.objects.filter(username=username).exists():
        User.objects.create_user(
            username=username,
            email='test5@example.com',
            password=password
        )
        print(f'Created test user: {username}')
    
    # Create test course if needed
    slug = 'python-fullstack'
    if not Course.objects.filter(slug=slug).exists():
        Course.objects.create(
            name='Python Fullstack Test',
            slug=slug,
            discounted_price='199.00',
            is_active=True
        )
        print(f'Created test course: {slug}')
    
    # Login and create order
    c = Client()
    logged = c.login(username=username, password=password)
    print('Logged in:', logged)
    
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
    
    # POST to create-order endpoint
    print('\nSending create-order request...')
    resp = c.post(
        f'/course/{slug}/create-order/',
        data=json.dumps(payload),
        content_type='application/json'
    )
    
    print(f'Status: {resp.status_code}')
    print(f'Response: {resp.content.decode("utf-8")}')

if __name__ == '__main__':
    main()