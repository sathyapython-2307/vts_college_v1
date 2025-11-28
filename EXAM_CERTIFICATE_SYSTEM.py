"""
EXAM CERTIFICATE SYSTEM - IMPLEMENTATION GUIDE

This module documents the Exam Certificate System implementation that stores
and manages certificates for students who scored 80% and above on exams.

================================================================================
OVERVIEW
================================================================================

The Exam Certificate System allows:
1. Automatic certificate creation for students scoring 80%+
2. Admin management of certificates with Excel export
3. Certificate file upload by admins
4. User-side certificate download in Achievements section
5. Comprehensive student information tracking

================================================================================
DATABASE MODELS
================================================================================

ExamCertificate Model:
  - Stores complete student and exam details for passing students
  - Links to ExamAttempt via OneToOneField
  - Fields include:
    * Student info: name, email, phone
    * Course info: name, duration (days & months)
    * Exam details: score %, questions, time taken
    * Violation tracking: type, count, details
    * Certificate file: uploaded by admin
    * Metadata: created_at, updated_at, is_active, admin_notes

Indexes:
  - student_email (for quick lookups)
  - is_active (for filtering)
  - -exam_submitted_date (for sorting)

================================================================================
ADMIN INTERFACE - FEATURES
================================================================================

Location: Django Admin > Core > Exam Certificates

LIST VIEW:
  - Display: Student name, course, score %, email, submission date, status
  - Filters: Active/Inactive, Violations, Submission date, Course name
  - Search: Student name, email, course name
  - Actions:
    * Download single certificate as Excel
    * Download multiple certificates as bulk Excel
    * Mark as active/inactive

DETAIL VIEW:
  - Read-only fields: All student, course, and exam details
  - Editable fields:
    * certificate_file: Upload PDF/JPG/PNG
    * admin_notes: Add admin comments
    * is_active: Toggle certificate validity

EXCEL EXPORT:
  - Includes all student information
  - Columns: Name, Email, Phone, Course, Duration, Score, Questions, Violations, etc.
  - Works for single or bulk exports
  - Auto-formats column widths

================================================================================
AUTOMATIC CERTIFICATE CREATION
================================================================================

Certificates are automatically created in two ways:

1. SIGNAL-BASED (Real-time):
   - When ExamAttempt is saved with is_passed=True and score_percentage >= 80
   - Signal handler: auto_create_certificate_on_pass()
   - Location: core/signals.py

2. MANAGEMENT COMMAND (Bulk):
   Command: python manage.py populate_exam_certificates
   
   Options:
     --course_id=N       Process only course N
     --user_id=N         Process only user N
     --recreate          Delete and recreate all certificates
   
   Examples:
     # Process all passing attempts
     python manage.py populate_exam_certificates
     
     # Process specific course
     python manage.py populate_exam_certificates --course_id=1
     
     # Recreate all certificates
     python manage.py populate_exam_certificates --recreate

================================================================================
CERTIFICATE UTILITIES
================================================================================

Location: core/certificate_utils.py

Available Functions:

get_passing_attempts(min_score=80, course_id=None, user_id=None)
  - Fetch exam attempts meeting passing criteria
  - Returns QuerySet of ExamAttempt objects

create_certificate_from_attempt(attempt, force_update=False)
  - Create/update certificate from single exam attempt
  - Returns (certificate, created) tuple

bulk_create_certificates(attempts)
  - Create certificates for multiple attempts
  - Returns stats dict with counts

get_student_certificates(user)
  - Get all active certificates for a user
  - Returns QuerySet of ExamCertificate objects

get_certificate_stats()
  - Get overall statistics
  - Returns dict with totals, averages, etc.

search_certificates(query, search_fields=None)
  - Search certificates by name, email, course
  - Returns QuerySet of matches

export_certificates_to_excel(certificates, include_violations=True)
  - Prepare data for Excel export
  - Returns list of dictionaries

================================================================================
USER-SIDE INTEGRATION
================================================================================

Location: templates/my_purchase.html

ACHIEVEMENTS TAB:
  - Shows two sections:
    1. Exam Certificates (80%+ scores)
    2. Course Certificates (completion certificates)
  
  Features:
    - Card display with score badge
    - Download button if certificate file uploaded
    - "Pending" message if awaiting admin upload
    - Violation indicators
    - Exam performance details

CERTIFICATE DOWNLOAD:
  - URL: /certificate/<certificate_id>/download/
  - View: core.views.download_exam_certificate
  - Access: Only certificate owner or admin
  - Returns file with name: {student_name}_certificate_{id}.pdf

================================================================================
API ENDPOINTS
================================================================================

Certificate Download:
  GET /certificate/<certificate_id>/download/
  - Returns certificate file
  - Only accessible to certificate owner or admin
  - Logs download activity

My Purchase (with certificates):
  GET /my-purchase/
  - Shows user's courses and certificates
  - Includes exam_certificates context

My Results:
  GET /my-results/
  - Shows submitted exam attempts

================================================================================
SETUP INSTRUCTIONS
================================================================================

1. MIGRATION:
   python manage.py migrate
   - Creates ExamCertificate table with indexes

2. AUTO-CREATE EXISTING CERTIFICATES:
   python manage.py populate_exam_certificates
   - Creates certificates for students who already passed exams

3. ADMIN SETUP:
   - Go to Django Admin > Core > Exam Certificates
   - Review list of passing students
   - Upload certificate files for each student

4. USER NOTIFICATION (Optional):
   - Can send email when certificate is uploaded
   - Hook: signals.certificate_file_upload_notification()

================================================================================
FEATURES & CAPABILITIES
================================================================================

STUDENT INFORMATION TRACKING:
  ✓ Full name, email, phone number
  ✓ Purchase/enrollment date
  ✓ Course name and duration (days → months calculation)

EXAM PERFORMANCE DETAILS:
  ✓ Score percentage
  ✓ Correct/total answers
  ✓ Time taken (minutes)
  ✓ Submission timestamp

SECURITY & VIOLATIONS:
  ✓ Tracks all violations during exam
  ✓ Violation types and counts
  ✓ Detailed violation descriptions
  ✓ JSON storage for complex data

ADMIN FEATURES:
  ✓ Certificate file upload (PDF/JPG/PNG)
  ✓ Admin notes field
  ✓ Activation/deactivation toggle
  ✓ Advanced filtering and search
  ✓ Bulk Excel export
  ✓ Single Excel export
  ✓ Custom admin actions

USER FEATURES:
  ✓ View certificates in Achievements tab
  ✓ Download certificate file
  ✓ See exam performance details
  ✓ Track violation history
  ✓ Easy-to-use interface

================================================================================
VIEWS FLOW
================================================================================

Admin Workflow:
1. Student takes exam and scores 80%+
2. Certificate auto-created by signal
3. Admin goes to Admin Panel > Exam Certificates
4. Finds student in list
5. Uploads certificate file
6. Saves (certificate_uploaded_date auto-set)
7. Certificate immediately visible to user

Student Workflow:
1. Takes exam and scores 80%+
2. Certificate auto-created
3. Visits My Purchase > Achievements
4. Sees certificate card
5. If certificate file uploaded: "Download" button available
6. If pending: "Pending upload" message shown
7. Downloads certificate file

Admin Bulk Export:
1. Navigate to Exam Certificates admin
2. Filter/search as needed
3. Select one or more certificates
4. Choose "Download as Excel" action
5. Excel file generated and downloaded

================================================================================
ERROR HANDLING
================================================================================

Signal Handler:
- Gracefully handles missing data
- Catches exceptions and logs them
- Doesn't interrupt exam submission

Certificate Creation:
- Validates score >= 80%
- Checks for existing certificates
- Returns detailed error messages
- Supports transaction rollback

File Upload:
- Validates file types (PDF, JPG, PNG)
- Prevents overwrite without confirmation
- Logs all file operations
- Handles missing files gracefully

================================================================================
PERFORMANCE CONSIDERATIONS
================================================================================

Indexing:
  - student_email: Fast user lookups
  - is_active: Quick filtering for active certs
  - -exam_submitted_date: Efficient sorting

Query Optimization:
  - select_related() for foreign keys
  - prefetch_related() for reverse relations
  - Efficient aggregation queries

Caching:
  - Consider caching certificate stats
  - Redis/Memcached friendly
  - Manual invalidation on updates

================================================================================
SECURITY NOTES
================================================================================

Access Control:
  - Users can only download their own certificates
  - Admin can download any certificate
  - Staff-only admin interface

Data Protection:
  - Student info stored securely
  - Violations tracked but not punitive
  - Admin notes protected
  - File uploads validated

================================================================================
FUTURE ENHANCEMENTS
================================================================================

Potential additions:
1. Certificate generation PDF on-the-fly
2. Email notifications when certificates ready
3. Certificate preview before download
4. Batch certificate generation
5. Certificate template customization
6. Digital signatures
7. Certificate verification code
8. Blockchain integration (optional)
9. Analytics dashboard
10. Certificate expiration tracking

================================================================================
TROUBLESHOOTING
================================================================================

Certificates not appearing:
  - Check if exam score is >= 80%
  - Verify exam is marked as submitted
  - Check is_passed flag
  - Run: python manage.py populate_exam_certificates

Excel export fails:
  - Verify pandas is installed
  - Check file permissions
  - Review logs for details
  - Ensure sufficient disk space

Certificate file won't upload:
  - Check file type (PDF/JPG/PNG only)
  - Verify file size
  - Check media folder permissions
  - Review Django settings for MEDIA_ROOT

Users can't download:
  - Verify certificate_file is set
  - Check URL routing
  - Verify user authentication
  - Check file permissions

================================================================================
CONTACT & SUPPORT
================================================================================

For issues or questions about the certificate system:
1. Check logs: python manage.py logs | grep certificate
2. Review model validation
3. Verify migration was applied
4. Test with populate_exam_certificates command
5. Check Django admin interface

================================================================================
"""


# This file serves as documentation reference for the Exam Certificate System
# Implementation. It is not executable Python code but provides comprehensive
# guidance on all aspects of the certificate management system.

if __name__ == '__main__':
    print(__doc__)
