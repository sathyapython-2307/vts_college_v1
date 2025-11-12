"""Test just the Razorpay payment API."""
import os
import sys
import json
import django
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

def test_razorpay_api():
    """Test direct Razorpay API access using configured credentials."""
    try:
        import razorpay
        from django.conf import settings
        
        print("\nRazorpay Settings Test:")
        print("-" * 50)
        print(f"RAZORPAY_ENABLED = {getattr(settings, 'RAZORPAY_ENABLED', None)}")
        print(f"RAZORPAY_KEY_ID = {getattr(settings, 'RAZORPAY_KEY_ID', None)}")
        print(f"RAZORPAY_KEY_SECRET length = {len(getattr(settings, 'RAZORPAY_KEY_SECRET', ''))}")
        print(f"RAZORPAY_CURRENCY = {getattr(settings, 'RAZORPAY_CURRENCY', None)}")
        
        key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
        key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
        
        if not key_id or not key_secret:
            print("\nError: Missing Razorpay credentials")
            return
            
        print("\nInitializing Razorpay client...")
        client = razorpay.Client(auth=(key_id, key_secret))
        
        print("Testing API access (fetching payments)...")
        payments = client.payment.all({'count': 1})
        print(f"Success! Retrieved {len(payments['items'])} payments")
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == '__main__':
    test_razorpay_api()