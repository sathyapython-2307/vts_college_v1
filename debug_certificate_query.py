#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import ExamCertificate

# Get u1 user
user = User.objects.get(email='u1@gmail.com')
print(f'User: {user.username} ({user.email})')
print()

# Check all certificates for this user
print('=== ALL Certificates for this user ===')
certs_all = ExamCertificate.objects.filter(exam_attempt__course_access__user=user)
print(f'Total: {certs_all.count()}')
for cert in certs_all:
    file_name = cert.certificate_file.name if cert.certificate_file else '[No file]'
    print(f'  - {cert.course_name} | is_active={cert.is_active} | file={file_name}')

print()

# Check only active certificates
print('=== ACTIVE Certificates (is_active=True) ===')
certs_active = ExamCertificate.objects.filter(exam_attempt__course_access__user=user, is_active=True)
print(f'Total: {certs_active.count()}')
for cert in certs_active:
    file_name = cert.certificate_file.name if cert.certificate_file else '[No file]'
    print(f'  - {cert.course_name} | file={file_name}')
