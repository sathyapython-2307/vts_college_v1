"""Test script for Razorpay signature verification."""
import os
import sys
import json
from pathlib import Path
import hmac
import hashlib
import django

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.conf import settings
import razorpay

def check_razorpay_config():
    """Check that Razorpay is properly configured."""
    print("\nChecking Razorpay Configuration")
    print("-" * 50)
    
    # Check if razorpay package is installed
    if razorpay is None:
        print("ERROR: Razorpay package not installed")
        return False
    print("✓ Razorpay package installed")
    
    # Check if settings are enabled
    if not getattr(settings, 'RAZORPAY_ENABLED', False):
        print("ERROR: Razorpay not enabled in settings")
        return False
    print("✓ Razorpay enabled in settings")
    
    # Check credentials
    key_id = getattr(settings, 'RAZORPAY_KEY_ID', '')
    key_secret = getattr(settings, 'RAZORPAY_KEY_SECRET', '')
    
    if not key_id:
        print("ERROR: RAZORPAY_KEY_ID not set")
        return False
    print("✓ RAZORPAY_KEY_ID configured")
    
    if not key_secret:
        print("ERROR: RAZORPAY_KEY_SECRET not set")
        return False
    print("✓ RAZORPAY_KEY_SECRET configured")
    
    return True

def test_order_creation(client):
    """Test creating a Razorpay order."""
    print("\nTesting Order Creation")
    print("-" * 50)
    
    order_data = {
        'amount': 50000,  # Rs. 500.00
        'currency': 'INR',
        'receipt': 'test_receipt_1',
        'payment_capture': 1,
        'notes': {
            'test_mode': True,
            'purpose': 'signature_verification_test'
        }
    }
    
    try:
        order = client.order.create(data=order_data)
        print(f"✓ Order created successfully")
        print(f"  Order ID: {order['id']}")
        print(f"  Amount: {order['amount']/100} {order['currency']}")
        return order
    except Exception as e:
        print(f"ERROR: Order creation failed - {str(e)}")
        return None

def test_signature_verification(client, order, key_secret):
    """Test signature generation and verification."""
    print("\nTesting Signature Verification")
    print("-" * 50)
    
    # Create a mock payment ID (in reality this comes from Razorpay)
    payment_id = f"pay_test_{order['id'][-8:]}"
    
    # Generate signature (simulating what Razorpay does)
    message = f"{order['id']}|{payment_id}"
    signature = hmac.new(
        key_secret.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Create webhook payload
    params_dict = {
        'razorpay_order_id': order['id'],
        'razorpay_payment_id': payment_id,
        'razorpay_signature': signature
    }
    
    print("Test parameters:")
    print(f"  Order ID:   {params_dict['razorpay_order_id']}")
    print(f"  Payment ID: {params_dict['razorpay_payment_id']}")
    print(f"  Signature:  {params_dict['razorpay_signature']}")
    
    try:
        # Test valid signature
        client.utility.verify_payment_signature(params_dict)
        print("✓ Valid signature verified successfully")
        
        # Test invalid signature
        invalid_params = params_dict.copy()
        invalid_params['razorpay_signature'] = 'invalid_signature'
        try:
            client.utility.verify_payment_signature(invalid_params)
            print("ERROR: Invalid signature was incorrectly verified")
        except:
            print("✓ Invalid signature correctly rejected")
            
        # Test missing signature
        missing_params = params_dict.copy()
        del missing_params['razorpay_signature']
        try:
            client.utility.verify_payment_signature(missing_params)
            print("ERROR: Missing signature was incorrectly processed")
        except:
            print("✓ Missing signature correctly rejected")
            
    except Exception as e:
        print(f"ERROR: Signature verification failed - {str(e)}")

def main():
    """Run full Razorpay integration test suite."""
    if not check_razorpay_config():
        print("\nCannot proceed with tests - configuration invalid")
        return
    
    try:
        key_id = settings.RAZORPAY_KEY_ID
        key_secret = settings.RAZORPAY_KEY_SECRET
        client = razorpay.Client(auth=(key_id, key_secret))
        
        # Test creating an order
        order = test_order_creation(client)
        if not order:
            print("\nCannot proceed with signature tests - order creation failed")
            return
            
        # Test signature verification
        test_signature_verification(client, order, key_secret)
        
    except Exception as e:
        print(f"\nUnexpected error during testing: {str(e)}")

if __name__ == '__main__':
    main()