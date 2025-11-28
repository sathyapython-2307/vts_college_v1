"""
QUICK START - EXAM CERTIFICATE SYSTEM

Get the certificate system up and running in 5 minutes.

================================================================================
STEP 1: APPLY MIGRATIONS (1 minute)
================================================================================

Run migration to create database table:

    python manage.py migrate

Expected output:
    Applying core.0027_examcertificate_delete_examcertificaterecord_and_more... OK


================================================================================
STEP 2: CREATE INITIAL CERTIFICATES (1 minute)
================================================================================

Populate certificates for students who already passed exams:

    python manage.py populate_exam_certificates

Expected output:
    Found X passing exam attempt(s)...
    ✓ Created certificate for student@email.com (Course Name - 95.00%)
    ✓ Created certificate for another@email.com (Course Name - 100.00%)
    
    ============================================================
    Created: X, Updated: 0, Skipped: 0
    ============================================================


================================================================================
STEP 3: VERIFY IN ADMIN (1 minute)
================================================================================

1. Start development server:
       python manage.py runserver

2. Go to admin:
       http://localhost:8000/admin/

3. Login with admin credentials

4. Navigate to:
       Core → Exam Certificates

You should see a list of certificates with:
  - Student names
  - Courses
  - Exam scores
  - Submission dates
  - Status (pending/uploaded)


================================================================================
STEP 4: UPLOAD A CERTIFICATE (1 minute)
================================================================================

1. Click on any certificate in the list

2. Scroll to "Certificate" section

3. Click "Choose File" and select a PDF, JPG, or PNG

4. Add optional admin notes in "Admin Notes" field

5. Click "Save"

6. Confirmation message should appear


================================================================================
STEP 5: VERIFY USER CAN DOWNLOAD (1 minute)
================================================================================

1. Log out of admin

2. Log in as the student user (whose certificate you uploaded)

3. Go to "My Purchase" page

4. Click "Achievements" tab

5. Under "Exam Certificates" section, you should see:
   - Card showing course name
   - Score badge
   - Exam submission date
   - "Download Certificate" button

6. Click download button - file should download


================================================================================
DONE! SYSTEM IS READY.
================================================================================

What's now available:

✓ Admin can view all 80%+ passing students
✓ Admin can upload certificates for each student
✓ Students can see their certificates
✓ Students can download certificate files
✓ Admin can export to Excel (single or bulk)
✓ Certificates auto-create when students pass exams


================================================================================
NEXT STEPS
================================================================================

For more detailed information:

1. ADMIN GUIDE:
   See EXAM_CERTIFICATE_SYSTEM.py section "ADMIN INTERFACE - FEATURES"

2. API REFERENCE:
   See CERTIFICATE_API_REFERENCE.py for programmatic usage

3. SETUP GUIDE:
   See SETUP_DEPLOYMENT_GUIDE.py for detailed setup

4. IMPLEMENTATION DETAILS:
   See IMPLEMENTATION_SUMMARY.py for complete documentation


================================================================================
COMMON TASKS
================================================================================

UPLOAD CERTIFICATE FOR STUDENT:
  1. Admin panel → Core → Exam Certificates
  2. Find student
  3. Click to open detail view
  4. Upload file
  5. Save

DOWNLOAD ALL CERTIFICATES AS EXCEL:
  1. Admin panel → Core → Exam Certificates
  2. Select all (or specific ones)
  3. Choose "Download as bulk Excel"
  4. File downloads

CREATE NEW CERTIFICATES (for existing passing exams):
  python manage.py populate_exam_certificates

CREATE CERTIFICATES FOR SPECIFIC COURSE:
  python manage.py populate_exam_certificates --course_id=5

VIEW CERTIFICATE STATISTICS:
  python manage.py shell
  >>> from core.certificate_utils import get_certificate_stats
  >>> print(get_certificate_stats())


================================================================================
TROUBLESHOOTING
================================================================================

CERTIFICATES NOT SHOWING:
  1. Verify exam score >= 80%
  2. Check exam is marked as submitted
  3. Run: python manage.py populate_exam_certificates

EXCEL EXPORT FAILS:
  1. Ensure pandas installed: pip install pandas openpyxl
  2. Check file permissions on media folder

FILE UPLOAD FAILS:
  1. Only PDF, JPG, PNG allowed
  2. Check media folder exists
  3. Verify media folder is writable

STUDENTS CAN'T DOWNLOAD:
  1. Verify certificate_file was uploaded
  2. Check file exists in media folder
  3. Verify user is logged in


================================================================================
"""


if __name__ == '__main__':
    print(__doc__)
