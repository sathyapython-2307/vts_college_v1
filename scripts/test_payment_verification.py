"""Test Razorpay payment verification."""
import os
import sys
import django
import json
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
import razorpay

def test_payment_verification():
    """Test the payment verification process."""
    from django.conf import settings
    
    print("\nRazorpay Payment Verification Test")
    print("-" * 50)
    
    # Initialize Razorpay client
    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    
    # Create test order first
    order_amount = 19900  # Rs. 199.00
    order_data = {
        'amount': order_amount,
        'currency': 'INR',
        'payment_capture': 1
    }
    
    print("Creating test order...")
    order = client.order.create(data=order_data)
    print(f"Order created: {order['id']}")
    
    # Now simulate payment verification
    # In reality, these values would come from the frontend after payment
    test_data = {
        'razorpay_payment_id': 'pay_dummy',
        'razorpay_order_id': order['id'],
        'razorpay_signature': 'dummy_sig'  # This will fail verification, but that's expected
    }
    
    print("\nTesting verification with Django view...")
    
    # Create test user and course if needed
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
    c = Client()
    success = c.login(username=username, password=password)
    print(f"Login successful: {success}")
    
    # Test the callback endpoint
    response = c.post(
        f'/course/{course.slug}/payment/callback/',
        data=json.dumps(test_data),
        content_type='application/json'
    )
    
    print("\nResponse from callback:")
    print(f"Status Code: {response.status_code}")
    print(f"Content: {response.content.decode('utf-8')}")

if __name__ == '__main__':
    test_payment_verification()