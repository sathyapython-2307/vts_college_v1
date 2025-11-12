"""
Quick script to test Razorpay key configuration.
"""
import razorpay

# Test credentials
key_id = 'rzp_test_RYnB6bkmpifFj4'
key_secret = '4oKd2Eg9xRHnzsSK7IzD2xKD'

try:
    # Initialize client
    print(f'Initializing Razorpay client with key_id={key_id}...')
    client = razorpay.Client(auth=(key_id, key_secret))
    
    # Test API call
    print('Testing client with payments.all()...')
    result = client.payment.all({'count': 1})
    print('Success! API responded:', result)
    
except Exception as e:
    print('Error:', str(e))