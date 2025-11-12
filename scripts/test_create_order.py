import os
import django
import json
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from core.models import Course

User = get_user_model()
user, created = User.objects.get_or_create(username='testbuyer', defaults={'email':'testbuyer@example.com'})
user.set_password('testpass')
user.save()

client = Client()
logged_in = client.login(username='testbuyer', password='testpass')
print('logged_in:', logged_in)

course = Course.objects.filter(is_active=True).first()
if not course:
    course = Course.objects.create(name='Test Course', discounted_price=100.00, is_active=True)
    print('created course with slug', course.slug)
else:
    print('using course', course.slug)

url = f'/course/{course.slug}/create-order/'
data = json.dumps({'first_name':'T','last_name':'B','email':'testbuyer@example.com','phone':'9999999999'})
resp = client.post(url, data, content_type='application/json')
print('response:', resp.content.decode())

from django.conf import settings as djsettings
print('SCRIPT RAZORPAY_SETTINGS =', getattr(djsettings, 'RAZORPAY_SETTINGS', None))
print('SCRIPT RAZORPAY_ENABLED =', getattr(djsettings, 'RAZORPAY_ENABLED', None))
print('SCRIPT RAZORPAY_KEY_ID =', getattr(djsettings, 'RAZORPAY_KEY_ID', None))

import core.views as core_views
print('core.views.get_config is', callable(getattr(core_views, 'get_config', None)))

resp = client.post(url, data, content_type='application/json')
