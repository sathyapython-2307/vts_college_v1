#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import ExamCertificate

# Get u1 user
user = User.objects.get(email='u1@gmail.com')

# Get exam certificates 
certs = ExamCertificate.objects.filter(
    exam_attempt__course_access__user=user,
    is_active=True
)

for cert in certs:
    print(f"Certificate ID: {cert.id}")
    print(f"Course: {cert.course_name}")
    print(f"Score: {cert.exam_score_percentage}%")
    print()
    print(f"certificate_file value: {cert.certificate_file}")
    print(f"certificate_file type: {type(cert.certificate_file)}")
    print(f"certificate_file.name: {cert.certificate_file.name if cert.certificate_file else 'NONE'}")
    print(f"bool(certificate_file): {bool(cert.certificate_file)}")
    print(f"certificate_file == '': {cert.certificate_file == ''}")
    print()
    print(f"In Django template, this would evaluate as:")
    if cert.certificate_file:
        print("  ✓ Truthy - DOWNLOAD BUTTON SHOWN")
    else:
        print("  ✗ Falsy - PENDING MESSAGE SHOWN")
