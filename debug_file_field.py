#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from core.models import ExamCertificate
from django.conf import settings

cert = ExamCertificate.objects.get(id=1)
print(f"Certificate ID: {cert.id}")
print(f"certificate_file value: {repr(cert.certificate_file)}")
print(f"certificate_file.name: {cert.certificate_file.name}")
print(f"Media root: {settings.MEDIA_ROOT}")
print()

# Check full path
full_path = os.path.join(settings.MEDIA_ROOT, cert.certificate_file.name)
print(f"Expected full path: {full_path}")
print(f"Path exists: {os.path.exists(full_path)}")
print()

# Check what Django thinks
print(f"certificate_file.size: {cert.certificate_file.size}")
print(f"certificate_file.url: {cert.certificate_file.url}")
print(f"bool(certificate_file): {bool(cert.certificate_file)}")
print(f"certificate_file storage: {cert.certificate_file.storage}")

# Try accessing the file
try:
    with cert.certificate_file.open('rb') as f:
        data = f.read()
        print(f"File accessible: ✓ (size: {len(data)} bytes)")
except Exception as e:
    print(f"File accessible: ✗ ({e})")
