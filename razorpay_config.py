"""Razorpay configuration module."""

# Test Mode Configuration
TEST_CONFIG = {
    'ENABLED': True,
    'KEY_ID': 'rzp_test_RYnB6bkmpifFj4',
    'KEY_SECRET': '4oKd2Eg9xRHnzsSK7IzD2xKD',
    'CURRENCY': 'INR'
}

# Production Mode Configuration (fill these in when going live)
PROD_CONFIG = {
    'ENABLED': False,
    'KEY_ID': '',
    'KEY_SECRET': '',
    'CURRENCY': 'INR'
}

def get_config(test_mode=True):
    """Get the appropriate Razorpay configuration."""
    return TEST_CONFIG if test_mode else PROD_CONFIG