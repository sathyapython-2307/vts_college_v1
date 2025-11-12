"""Verify Razorpay configuration is loaded correctly."""
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

from django.conf import settings

print("\nRazorpay Configuration Check:")
print("-" * 50)

# Check for individual settings
print("RAZORPAY_ENABLED =", getattr(settings, 'RAZORPAY_ENABLED', None))
print("RAZORPAY_KEY_ID =", getattr(settings, 'RAZORPAY_KEY_ID', None))
print("RAZORPAY_KEY_SECRET =", bool(getattr(settings, 'RAZORPAY_KEY_SECRET', None)))
print("RAZORPAY_CURRENCY =", getattr(settings, 'RAZORPAY_CURRENCY', None))

# Check for settings dict
razorpay_settings = getattr(settings, 'RAZORPAY_SETTINGS', {})
print("\nRAZORPAY_SETTINGS dict:")
print("ENABLED =", razorpay_settings.get('ENABLED'))
print("KEY_ID =", razorpay_settings.get('KEY_ID'))
print("KEY_SECRET present =", bool(razorpay_settings.get('KEY_SECRET')))
print("CURRENCY =", razorpay_settings.get('CURRENCY'))

# Try importing razorpay
try:
    import razorpay
    print("\nrazorpay package is installed")
except ImportError:
    print("\nrazorpay package is NOT installed")