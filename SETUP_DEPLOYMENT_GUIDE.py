"""
EXAM CERTIFICATE SYSTEM - SETUP & DEPLOYMENT GUIDE

Complete step-by-step guide for deploying and using the Exam Certificate System.

================================================================================
QUICK START (5 MINUTES)
================================================================================

1. APPLY MIGRATIONS
   cd /path/to/project
   python manage.py migrate
   
   Output should show:
   Applying core.0027_examcertificate_delete_examcertificaterecord_and_more... OK


2. CREATE CERTIFICATES FOR EXISTING PASSING STUDENTS
   python manage.py populate_exam_certificates
   
   Output:
   Found X passing exam attempt(s)...
   Created: X, Updated: 0, Skipped: 0


3. VERIFY IN ADMIN
   - Start development server: python manage.py runserver
   - Go to http://localhost:8000/admin/
   - Navigate to "Core" > "Exam Certificates"
   - You should see a list of certificates


4. UPLOAD CERTIFICATE FOR A STUDENT
   - Click on any certificate
   - Scroll to "Certificate" section
   - Click "Upload certificate file"
   - Select PDF/JPG/PNG file
   - Click "Save"
   - Student can now download from their profile


5. USER VERIFICATION
   - Log in as student user
   - Navigate to "My Purchase" page
   - Click "Achievements" tab
   - See certificate with download button

================================================================================
DETAILED SETUP INSTRUCTIONS
================================================================================

STEP 1: PRE-REQUIREMENTS
========================

Ensure installed packages:
  - Django (latest)
  - pandas (for Excel export)
  - openpyxl (for Excel writing)

Check installations:
  pip list | grep -E "Django|pandas|openpyxl"

If missing, install:
  pip install pandas openpyxl


STEP 2: DATABASE MIGRATION
===========================

Apply all migrations:
  python manage.py migrate

Verify migration applied:
  python manage.py showmigrations core
  
Should show:
  [X] 0027_examcertificate_delete_examcertificaterecord_and_more


STEP 3: POPULATE EXISTING CERTIFICATES
========================================

For existing exam data, populate certificates:
  python manage.py populate_exam_certificates

With options:
  # Specific course
  python manage.py populate_exam_certificates --course_id=1
  
  # Specific user
  python manage.py populate_exam_certificates --user_id=1
  
  # Recreate all (warning: destructive)
  python manage.py populate_exam_certificates --recreate


STEP 4: ADMIN INTERFACE SETUP
==============================

1. Start Django development server:
   python manage.py runserver

2. Access admin panel:
   http://localhost:8000/admin/

3. Navigate to: Core > Exam Certificates

4. You should see:
   - List of all student certificates
   - Filter options (status, violations, date, course)
   - Search by name, email, course
   - Bulk action options
   - Download Excel button

5. For each certificate:
   - Click to open detail view
   - Scroll to "Certificate" section
   - Choose file to upload
   - Add admin notes if needed
   - Save

6. File upload:
   - Accepted formats: PDF, JPG, PNG
   - Max size: Django FILE_UPLOAD_MAX_MEMORY_SIZE
   - Directory: media/exam_certificates/YYYY/MM/DD/


STEP 5: CONFIGURE MEDIA STORAGE
================================

Ensure MEDIA_ROOT and MEDIA_URL in settings.py:
  
  MEDIA_ROOT = BASE_DIR / 'media'
  MEDIA_URL = '/media/'

Create media directory:
  mkdir -p media/exam_certificates

For production (Render/AWS/etc):
  - Use appropriate storage backend
  - Configure file permissions
  - Set MEDIA_ROOT to persistent storage


STEP 6: VERIFY USER-SIDE FUNCTIONALITY
========================================

1. Log in as test student:
   - Use student credentials
   - Or create test account

2. Navigate to "My Purchase":
   http://localhost:8000/my-purchase/

3. Click "Achievements" tab:
   - Should see "Exam Certificates" section
   - Shows cards for each 80%+ exam
   - If certificate file uploaded: "Download" button
   - If pending: "Pending upload" message

4. Test download:
   - Click download button
   - File should download successfully
   - Check filename format

5. Verify data displayed:
   - Score percentage badge
   - Exam submission date
   - Correct/total questions
   - Violation indicators


STEP 7: EMAIL NOTIFICATIONS (OPTIONAL)
========================================

To notify users when certificates are ready:

1. Configure email backend in settings.py:
   EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
   EMAIL_HOST = 'smtp.gmail.com'
   EMAIL_PORT = 587
   EMAIL_USE_TLS = True
   EMAIL_HOST_USER = 'your-email@gmail.com'
   EMAIL_HOST_PASSWORD = 'your-password'

2. Create signal in core/signals.py:
   def send_certificate_ready_email(certificate):
       from django.core.mail import send_mail
       send_mail(
           'Your Certificate is Ready',
           f'Your certificate for {certificate.course_name} is ready to download',
           'admin@example.com',
           [certificate.student_email],
       )

3. Call from certificate upload:
   # In admin.py save_model()
   if 'certificate_file' in changed_data:
       send_certificate_ready_email(obj)


================================================================================
ADMIN INTERFACE GUIDE
================================================================================

ACCESSING ADMIN
===============

URL: /admin/core/examcertificate/

Default columns displayed:
  - Student Name
  - Course Name
  - Exam Score (%)
  - Email
  - Exam Submitted Date
  - Certificate Status (uploaded/pending)
  - Is Active

Sorting:
  - Click column header to sort
  - Default: sorted by submission date (newest first)

Filtering:
  Left sidebar offers filters:
  - Is Active: Show active/inactive
  - Has Violations: Filter by violation presence
  - Exam Submitted Date: Date range picker
  - Course Name: Course filter

Searching:
  - Search box at top
  - Searches: student_name, student_email, course_name
  - Example: search "python" finds all Python course certs


VIEWING CERTIFICATE DETAILS
=============================

Click on certificate to view full details:

Read-only sections:
  - Student Information (name, email, phone)
  - Course Information (name, duration)
  - Exam Performance (score, questions, time)
  - Security & Violations (expandable section)
  - Metadata (created/updated dates)

Editable sections:
  - Certificate File (upload)
  - Admin Notes (add comments)
  - Is Active (activate/deactivate)

Read-only with link:
  - Certificate File Preview (shows file link if uploaded)


UPLOADING CERTIFICATE FILE
============================

In detail view:
1. Find "Certificate" section
2. Drag-drop file or click "Choose File"
3. Select PDF, JPG, or PNG
4. Click "Save"
5. Confirmation shows:
   - File saved successfully
   - Certificate uploaded date auto-set
   - User can now download

File location:
  /media/exam_certificates/YYYY/MM/DD/filename.pdf


BULK ACTIONS
=============

Select multiple certificates using checkboxes:
1. Check certificates to select
2. Choose action from dropdown:
   - Download selected as Excel
   - Download selected as bulk Excel
   - Mark selected as active
   - Mark selected as inactive
3. Click "Go"
4. Action executes


EXCEL EXPORT
=============

Single certificate:
1. Select one certificate
2. Choose "Download single as Excel"
3. File generated and downloaded
4. Filename: {student_name}_certificate.xlsx

Bulk export:
1. Select multiple (or all)
2. Choose "Download as bulk Excel"
3. File generated with all selected
4. Filename: exam_certificates_bulk_YYYYMMDD_HHMMSS.xlsx

Columns in Excel:
  - Student Name, Email, Phone
  - Course Name, Duration (Days), Duration (Months)
  - Purchased Date, Joined Date
  - Exam Score (%), Correct Answers, Total Questions
  - Exam Duration (Minutes), Exam Submitted Date
  - Certificate Status
  - Violation info, Admin Notes


ADVANCED FEATURES
==================

Custom views URL:
  /admin/core/examcertificate/download-bulk-excel/
  
  Downloads all active certificates as Excel
  No selection needed
  Useful for bulk reporting


================================================================================
TESTING
================================================================================

MANUAL TESTING CHECKLIST
========================

() Admin list view displays correctly
() Filtering works (active, violations, date, course)
() Searching works (name, email, course)
() Sorting works (click headers)
() Certificate detail view shows all fields
() File upload accepts PDF/JPG/PNG
() File upload rejects other formats
() Excel export generates valid file
() Single export works
() Bulk export works
() User achievements page shows certificates
() Certificate download works for owner
() Certificate download blocked for other users
() Admin can download any certificate
() Violation details display correctly


AUTOMATED TESTING
=================

Create test case:
  
  # tests.py
  from django.test import TestCase
  from core.models import ExamCertificate, ExamAttempt
  from core.certificate_utils import get_passing_attempts
  
  class ExamCertificateTestCase(TestCase):
      def test_certificate_creation(self):
          # Create passing exam attempt
          # Verify certificate auto-created
          # Check all fields populated
          pass
      
      def test_certificate_score_validation(self):
          # Attempt with 79% score
          # Verify no certificate created
          pass
      
      def test_certificate_download(self):
          # Test user can download own
          # Test user cannot download other's
          # Test admin can download any
          pass

Run tests:
  python manage.py test core.tests


================================================================================
TROUBLESHOOTING
================================================================================

ISSUE: Certificates not appearing after exam
============================================

Solution 1: Check exam score >= 80%
  SELECT score_percentage FROM core_examattempt WHERE id=1;

Solution 2: Verify exam marked as submitted
  SELECT is_submitted, is_passed FROM core_examattempt WHERE id=1;

Solution 3: Run populate command
  python manage.py populate_exam_certificates

Solution 4: Check signal registration
  - Verify core/signals.py imports in apps.py
  - Check Django logs for signal errors


ISSUE: Excel export fails with "No module named pandas"
========================================================

Solution: Install pandas and openpyxl
  pip install pandas openpyxl

Verify installation:
  python -c "import pandas; import openpyxl; print('OK')"


ISSUE: Certificate file won't upload
====================================

Solution 1: Check file format
  Only PDF, JPG, PNG accepted

Solution 2: Verify media folder exists
  mkdir -p media/exam_certificates
  chmod 755 media/exam_certificates

Solution 3: Check Django settings
  Verify MEDIA_ROOT and MEDIA_URL set

Solution 4: Check file permissions
  ls -la media/
  chmod 777 media/

Solution 5: Check file size
  Verify FILE_UPLOAD_MAX_MEMORY_SIZE > file size


ISSUE: Users can't see certificates in "My Purchase"
====================================================

Solution 1: Verify context passed
  Check my_purchase view includes exam_certificates

Solution 2: Verify certificate is_active=True
  SELECT is_active FROM core_examcertificate;

Solution 3: Check template rendering
  - Verify my_purchase.html displays certificates
  - Check for JavaScript errors
  - Verify CSS not hiding content

Solution 4: Verify certificates exist for user
  SELECT * FROM core_examcertificate 
  WHERE exam_attempt_id IN (
    SELECT id FROM core_exaattempt 
    WHERE course_access_id IN (
      SELECT id FROM core_courseaccess 
      WHERE user_id = 1  -- your user id
    )
  );


ISSUE: Users can't download certificates
=========================================

Solution 1: Verify certificate_file uploaded
  SELECT certificate_file FROM core_examcertificate WHERE id=1;

Solution 2: Check file exists on disk
  ls -la media/exam_certificates/

Solution 3: Check URL configuration
  Verify certificate download URL in urls.py

Solution 4: Check view permissions
  - User must be authenticated
  - User must be certificate owner or admin

Solution 5: Check Django MEDIA configuration
  - MEDIA_ROOT correctly set
  - MEDIA_URL correctly set
  - Web server serving media files


================================================================================
MONITORING
================================================================================

LOG IMPORTANT EVENTS
====================

Configure logging in settings.py:

LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'certificates.log',
        },
    },
    'loggers': {
        'core.signals': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'core.admin': {
            'handlers': ['file'],
            'level': 'INFO',
        },
    },
}

View logs:
  tail -f certificates.log


CERTIFICATE STATISTICS
=======================

Get stats via Django shell:

python manage.py shell

> from core.certificate_utils import get_certificate_stats
> stats = get_certificate_stats()
> print(stats)

{
  'total_certificates': 100,
  'certificates_with_file': 85,
  'certificates_without_file': 15,
  'with_violations': 10,
  'average_score': 92.5
}


MONITOR STORAGE USAGE
=====================

Check media folder size:

du -sh media/exam_certificates/

Monitor database size:

SELECT COUNT(*) as total, 
       COUNT(CASE WHEN certificate_file != '' THEN 1 END) as with_file
FROM core_examcertificate;


================================================================================
PRODUCTION DEPLOYMENT
================================================================================

PRE-DEPLOYMENT CHECKLIST
=========================

() Database migrated: python manage.py migrate
() Static files collected: python manage.py collectstatic
() Media folder writable: chmod 755 media/
() Email configured (if notifications)
() Logging configured
() File upload size limits set
() Secure file permissions
() Test all functionality


ENVIRONMENT VARIABLES
======================

Set these for production:

ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-secure-key-here
DEBUG=False
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
SECURE_BROWSER_XSS_FILTER=True


STORAGE BACKENDS
=================

For AWS S3:

pip install boto3

In settings.py:
  DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
  AWS_STORAGE_BUCKET_NAME = 'your-bucket'
  AWS_S3_REGION_NAME = 'us-east-1'
  AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
  AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')

For Google Cloud Storage:

pip install django-storages

Similar configuration for GCS...


BACKUPS
=======

Backup database:
  python manage.py dumpdata core.ExamCertificate > certificates_backup.json

Backup media files:
  tar -czf media_backup.tar.gz media/exam_certificates/

Restore from backup:
  python manage.py loaddata certificates_backup.json
  tar -xzf media_backup.tar.gz

================================================================================
SUPPORT & DOCUMENTATION
================================================================================

Files included:
  - EXAM_CERTIFICATE_SYSTEM.py - Detailed documentation
  - CERTIFICATE_API_REFERENCE.py - API usage examples
  - core/models.py - ExamCertificate model definition
  - core/admin.py - Admin interface implementation
  - core/signals.py - Auto-creation logic
  - core/certificate_utils.py - Utility functions
  - core/management/commands/populate_exam_certificates.py - Bulk command

For questions or issues:
  1. Check documentation files
  2. Review Django logs
  3. Run: python manage.py check
  4. Test with populate command

================================================================================
"""


if __name__ == '__main__':
    print(__doc__)
