#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import CourseAccess, ExamCertificate

user = User.objects.get(email='u1@gmail.com')
print(f"User: {user.email}\n")

# Check course accesses
accesses = CourseAccess.objects.filter(user=user, is_active=True)
print(f"Active Course Accesses: {accesses.count()}")
for access in accesses:
    print(f"  - Course: {access.course.name if access.course else 'NO COURSE'}")
    print(f"    ID: {access.id}")
    print(f"    Payment: {access.payment}")
    print(f"    is_active: {access.is_active}")
    print()

# Check exam certificates
certs = ExamCertificate.objects.filter(exam_attempt__course_access__user=user)
print(f"\nExam Certificates: {certs.count()}")
for cert in certs:
    print(f"  - Certificate ID: {cert.id}")
    print(f"    Course Name: {cert.course_name}")
    print(f"    Score: {cert.exam_score_percentage}%")
    print(f"    Exam Attempt: {cert.exam_attempt_id}")
    print(f"    Course Access: {cert.exam_attempt.course_access}")
    print(f"    Course: {cert.exam_attempt.course_access.course}")
    print()

# Check the specific exam attempt and course access relationship
print("\nDetailed Exam Attempt Check:")
from core.models import ExamAttempt
attempts = ExamAttempt.objects.filter(course_access__user=user)
for attempt in attempts:
    print(f"  Attempt ID: {attempt.id}")
    print(f"  Course Access: {attempt.course_access}")
    print(f"  Course: {attempt.course_access.course}")
    print(f"  User: {attempt.course_access.user}")
    print(f"  Score: {attempt.score_percentage}%")
    print()
