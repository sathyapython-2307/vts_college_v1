#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Online_Course.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import CourseAccess

user = User.objects.get(email='u1@gmail.com')
accesses = CourseAccess.objects.filter(user=user, is_active=True)

for access in accesses:
    print(f"Course: {access.course.name}")
    print(f"Access ID: {access.id}")
    
    # Check progress
    try:
        prog = access.progress
        print(f"Progress object: {prog}")
        if hasattr(prog, 'progress_percentage'):
            print(f"  progress_percentage: {prog.progress_percentage}")
        print(f"  type: {type(prog)}")
    except Exception as e:
        print(f"  Error getting progress: {e}")
    
    # Check if progress > 0
    try:
        progress_value = float(getattr(access, 'progress', 0.0))
        print(f"Progress value (float): {progress_value}")
        print(f"Should show progress bar: {progress_value > 0}")
    except Exception as e:
        print(f"  Error: {e}")
