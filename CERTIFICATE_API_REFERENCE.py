"""
EXAM CERTIFICATE SYSTEM - API REFERENCE & USAGE EXAMPLES

Quick reference guide with practical code examples for using the
Exam Certificate System programmatically.

================================================================================
MODELS
================================================================================

ExamCertificate Model Structure:

from core.models import ExamCertificate

Fields:
  exam_attempt (OneToOneField): Link to ExamAttempt
  student_name (CharField): Student's full name
  student_email (EmailField): Student's email
  student_phone (CharField): Student's phone number
  
  course_name (CharField): Course name
  course_duration_days (IntegerField): Duration in days
  course_duration_months (DecimalField): Duration in months (calculated)
  
  purchased_date (DateTimeField): When purchased/enrolled
  joined_date (DateTimeField): When student joined
  
  exam_score_percentage (DecimalField): Score as percentage
  correct_answers (IntegerField): Number of correct answers
  total_questions (IntegerField): Total exam questions
  exam_duration_taken_minutes (IntegerField): Time to complete exam
  exam_submitted_date (DateTimeField): When exam was submitted
  
  has_violations (BooleanField): Whether any violations occurred
  violation_count (IntegerField): Total violations
  violation_details (TextField): JSON with violation details
  
  certificate_file (FileField): Uploaded certificate
  certificate_uploaded_date (DateTimeField): When certificate uploaded
  
  admin_notes (TextField): Admin comments
  is_active (BooleanField): Active/inactive status
  created_at (DateTimeField): Auto-set when created
  updated_at (DateTimeField): Auto-update when modified

================================================================================
BASIC USAGE EXAMPLES
================================================================================

1. RETRIEVE CERTIFICATES
   
   # Get all active certificates
   from core.models import ExamCertificate
   certs = ExamCertificate.objects.filter(is_active=True)
   
   # Get certificates for a specific user
   from django.contrib.auth.models import User
   user = User.objects.get(email='student@example.com')
   user_certs = ExamCertificate.objects.filter(
       exam_attempt__course_access__user=user
   )
   
   # Get certificates for a specific course
   from core.models import Course
   course = Course.objects.get(name='Python Basics')
   course_certs = ExamCertificate.objects.filter(
       course_name=course.name
   )
   
   # Get certificates with violations
   violation_certs = ExamCertificate.objects.filter(
       has_violations=True
   )


2. SEARCH CERTIFICATES
   
   from core.certificate_utils import search_certificates
   
   # Search by student name
   results = search_certificates('John Doe')
   
   # Search by email
   results = search_certificates('john@example.com')
   
   # Search by course
   results = search_certificates('Python')


3. GET CERTIFICATE STATISTICS
   
   from core.certificate_utils import get_certificate_stats
   
   stats = get_certificate_stats()
   # Returns:
   # {
   #     'total_certificates': 100,
   #     'certificates_with_file': 85,
   #     'certificates_without_file': 15,
   #     'with_violations': 10,
   #     'average_score': 92.5
   # }


4. CREATE CERTIFICATE PROGRAMMATICALLY
   
   from core.models import ExamAttempt, ExamCertificate
   from core.certificate_utils import create_certificate_from_attempt
   
   # Get a passing exam attempt
   attempt = ExamAttempt.objects.get(id=1)
   
   # Create certificate (if score >= 80%)
   try:
       cert, created = create_certificate_from_attempt(attempt)
       if created:
           print(f"Certificate created for {cert.student_name}")
       else:
           print(f"Certificate already exists")
   except ValueError as e:
       print(f"Cannot create certificate: {e}")


5. GET STUDENT'S CERTIFICATES
   
   from core.certificate_utils import get_student_certificates
   from django.contrib.auth.models import User
   
   user = User.objects.get(email='student@example.com')
   certificates = get_student_certificates(user)
   
   for cert in certificates:
       print(f"{cert.student_name} - {cert.course_name}: {cert.exam_score_percentage}%")


6. EXPORT TO EXCEL
   
   from core.certificate_utils import export_certificates_to_excel
   from core.models import ExamCertificate
   import pandas as pd
   
   certs = ExamCertificate.objects.filter(is_active=True)
   data = export_certificates_to_excel(certs)
   
   df = pd.DataFrame(data)
   df.to_excel('certificates.xlsx', index=False)


7. UPDATE CERTIFICATE
   
   from core.models import ExamCertificate
   
   cert = ExamCertificate.objects.get(id=1)
   cert.admin_notes = 'Certificate verified'
   cert.is_active = True
   cert.save()


8. UPLOAD CERTIFICATE FILE
   
   from core.models import ExamCertificate
   from django.core.files import File
   
   cert = ExamCertificate.objects.get(id=1)
   
   with open('certificate.pdf', 'rb') as f:
       cert.certificate_file.save('certificate.pdf', File(f))
   
   print(f"Certificate uploaded: {cert.certificate_file.url}")


9. BULK CERTIFICATE CREATION
   
   from core.certificate_utils import bulk_create_certificates
   from core.models import ExamAttempt
   from decimal import Decimal
   
   # Get all passing attempts
   passing_attempts = ExamAttempt.objects.filter(
       is_submitted=True,
       is_passed=True,
       score_percentage__gte=Decimal('80')
   )
   
   # Create certificates
   stats = bulk_create_certificates(passing_attempts)
   print(f"Created: {stats['created']}, Updated: {stats['updated']}, Skipped: {stats['skipped']}")


10. FILTER BY SCORE RANGE
    
    # Get certificates with 80-90% score
    certs_80_90 = ExamCertificate.objects.filter(
        exam_score_percentage__gte=80,
        exam_score_percentage__lt=90
    )
    
    # Get certificates with 90%+ score
    certs_90_plus = ExamCertificate.objects.filter(
        exam_score_percentage__gte=90
    )


11. FILTER BY DATE RANGE
    
    from datetime import datetime, timedelta
    
    # Get certificates from last 30 days
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_certs = ExamCertificate.objects.filter(
        exam_submitted_date__gte=thirty_days_ago
    )


12. GET VIOLATION DETAILS
    
    import json
    
    cert = ExamCertificate.objects.get(id=1)
    
    if cert.has_violations:
        violations = json.loads(cert.violation_details) if cert.violation_details else []
        for violation in violations:
            print(f"{violation['type']}: {violation['count']} times")


13. COUNT CERTIFICATES BY COURSE
    
    from django.db.models import Count
    
    course_stats = ExamCertificate.objects.values('course_name').annotate(
        count=Count('id')
    ).order_by('-count')
    
    for stat in course_stats:
        print(f"{stat['course_name']}: {stat['count']} certificates")


14. GET CERTIFICATES WITHOUT UPLOADED FILES
    
    from django.db.models import Q
    
    pending = ExamCertificate.objects.filter(
        Q(certificate_file='') | Q(certificate_file__isnull=True)
    )
    
    print(f"Pending certificates: {pending.count()}")


15. BULK UPDATE STATUS
    
    from core.models import ExamCertificate
    
    # Activate all certificates
    ExamCertificate.objects.all().update(is_active=True)
    
    # Deactivate old certificates
    from datetime import datetime, timedelta
    old_date = datetime.now() - timedelta(days=365)
    ExamCertificate.objects.filter(
        exam_submitted_date__lt=old_date
    ).update(is_active=False)

================================================================================
MANAGEMENT COMMANDS
================================================================================

1. POPULATE ALL CERTIFICATES
   
   python manage.py populate_exam_certificates
   
   Options:
     --course_id=1           Process only course 1
     --user_id=1             Process only user 1
     --recreate              Delete and recreate all


2. EXAMPLES
   
   # Create certificates for all passing students
   python manage.py populate_exam_certificates
   
   # Create certificates for specific course
   python manage.py populate_exam_certificates --course_id=5
   
   # Create certificates for specific student
   python manage.py populate_exam_certificates --user_id=10
   
   # Recreate all certificates (destructive)
   python manage.py populate_exam_certificates --recreate

================================================================================
VIEWS & URLS
================================================================================

1. VIEW CERTIFICATES IN DJANGO ADMIN
   
   URL: /admin/core/examcertificate/
   
   Features:
   - List all certificates with filters
   - Search by name, email, course
   - Download single certificate as Excel
   - Download multiple as bulk Excel
   - Upload certificate files
   - Add admin notes
   - Activate/deactivate certificates


2. USER ACHIEVEMENTS PAGE
   
   URL: /my-purchase/
   
   Features:
   - View all earned exam certificates
   - See exam scores and details
   - Download certificate files
   - View violation indicators


3. DOWNLOAD CERTIFICATE
   
   URL: /certificate/<certificate_id>/download/
   
   Usage:
   - Only certificate owner or admin can download
   - Returns PDF file
   - Filename: {student_name}_certificate_{id}.pdf

================================================================================
SIGNALS
================================================================================

Auto-create on Exam Pass:
   Triggered by: ExamAttempt post_save signal
   Condition: is_submitted=True, is_passed=True, score_percentage>=80
   Action: ExamCertificate created automatically
   Location: core/signals.py


Certificate File Upload Notification:
   Triggered by: ExamCertificate post_save signal
   Condition: certificate_file field changed
   Action: Can send notification email to user
   Location: core/signals.py

================================================================================
TEMPLATE CONTEXT VARIABLES
================================================================================

my_purchase.html context variables:

- exam_certificates: QuerySet of ExamCertificate for logged-in user
  Usage in template:
    {% for cert in exam_certificates %}
      {{ cert.student_name }}
      {{ cert.course_name }}
      {{ cert.exam_score_percentage }}
      {{ cert.certificate_file.url }}
    {% endfor %}

- certificates: QuerySet of legacy Certificate objects
  Usage in template:
    {% for cert in certificates %}
      {{ cert.get_certificate_type_display }}
    {% endfor %}

================================================================================
PERMISSIONS
================================================================================

Admin Access:
  - Staff users can access admin interface
  - All certificate management available
  - Can upload files, edit notes, manage status

User Access:
  - Users can view their own certificates
  - Users can download their own certificate files
  - Read-only access to certificate details

Unauthenticated:
  - No access to certificate data
  - Redirected to login for downloads

================================================================================
ERROR HANDLING
================================================================================

Common Errors and Solutions:

1. "Attempt score is below 80% threshold"
   Solution: Only attempts with score >= 80 can have certificates

2. "Attempt must be submitted and passed"
   Solution: Ensure exam is marked submitted and passed

3. "Certificate not found"
   Solution: Verify certificate ID exists and is_active=True

4. "You do not have permission to download"
   Solution: Must be certificate owner or admin staff

5. "Certificate file is not available yet"
   Solution: Admin must upload certificate file first

6. "Error downloading certificate"
   Solution: Check file permissions and Django MEDIA_ROOT settings

================================================================================
LOGGING
================================================================================

Certificate-related events are logged at:
  Logger: core.signals
  Logger: core.views
  Logger: core.admin

View logs:
  - Check Django logs for 'certificate' keyword
  - Review admin action logs
  - Check signal execution logs

================================================================================
PERFORMANCE TIPS
================================================================================

1. Use select_related for exam_attempt
2. Use prefetch_related for violations
3. Use only() to fetch specific fields
4. Cache certificate stats
5. Use database indexes (already created)
6. Batch operations for bulk creates
7. Limit queryset size for exports

================================================================================
TROUBLESHOOTING
================================================================================

Certificates not auto-creating:
  1. Check signal is registered in apps.py
  2. Verify exam score is >= 80%
  3. Check exam is_submitted and is_passed
  4. Review Django logs for errors

Bulk export not working:
  1. Verify pandas is installed
  2. Check file write permissions
  3. Ensure MEDIA_ROOT exists
  4. Review error logs

File upload fails:
  1. Check file type (PDF/JPG/PNG)
  2. Verify file size limit
  3. Check MEDIA_ROOT permissions
  4. Review storage backend settings

================================================================================
"""


if __name__ == '__main__':
    print(__doc__)
