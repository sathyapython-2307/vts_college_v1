#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import RequestFactory
from core.views import my_purchase
from django.template import Context, loader

# Create a fake request for user u1@gmail.com
user = User.objects.get(email='u1@gmail.com')
factory = RequestFactory()
request = factory.get('/my-purchase/')
request.user = user

print(f"Simulating request for user: {user.email}")
print()

# Call the view
response = my_purchase(request)

# Get context from response if it's a TemplateResponse
if hasattr(response, 'context_data'):
    context = response.context_data
else:
    print("Response doesn't have context_data - it might be a regular HttpResponse")
    exit(1)

print("Context data from view:")
print(f"  course_accesses: {len(context.get('course_accesses', []))} items")
print(f"  certificates: {len(context.get('certificates', []))} items")
print(f"  exam_certificates: {len(context.get('exam_certificates', []))} items")
print()

exam_certs = context.get('exam_certificates', [])
print(f"Exam Certificates ({len(exam_certs)}):")
for i, cert in enumerate(exam_certs):
    print(f"  [{i}] {cert.course_name} - {cert.exam_score_percentage}%")
    print(f"      certificate_file: {cert.certificate_file}")
    print(f"      bool(certificate_file): {bool(cert.certificate_file)}")
