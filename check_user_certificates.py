#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import ExamCertificate

user = User.objects.get(email='u1@gmail.com')
print(f"Checking certificates for user: {user.email}\n")

# Get exact query from view
exam_certificates = ExamCertificate.objects.filter(
    exam_attempt__course_access__user=user,
    is_active=True
).select_related('exam_attempt__course_access__course').order_by('-exam_submitted_date')

print(f"Query results: {exam_certificates.count()} certificates\n")

for i, cert in enumerate(exam_certificates):
    print(f"Certificate {i+1}:")
    print(f"  ID: {cert.id}")
    print(f"  Course: {cert.course_name}")
    print(f"  Score: {cert.exam_score_percentage}%")
    print(f"  is_active: {cert.is_active}")
    print(f"  certificate_file: {repr(cert.certificate_file)}")
    print(f"  certificate_file.name: {cert.certificate_file.name if cert.certificate_file else 'EMPTY'}")
    print(f"  bool(certificate_file): {bool(cert.certificate_file)}")
    print()
