import os
import django
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
try:
    django.setup()
    from django.conf import settings
    print('RAZORPAY_SETTINGS =', getattr(settings, 'RAZORPAY_SETTINGS', None))
    print('RAZORPAY_ENABLED =', getattr(settings, 'RAZORPAY_ENABLED', None))
    print('RAZORPAY_KEY_ID =', getattr(settings, 'RAZORPAY_KEY_ID', None))
    print('RAZORPAY_KEY_SECRET present =', bool(getattr(settings, 'RAZORPAY_KEY_SECRET', None)))
except Exception as e:
    print('ERROR:', e)
    sys.exit(1)
