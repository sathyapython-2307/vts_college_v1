"""
Signals for automatic certificate creation when exam attempts are passed.
Hooks into the ExamAttempt model to create certificates when:
1. Exam attempt is submitted
2. Score is 80% or above
3. is_passed flag is True
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
import json
import logging

from .models import ExamAttempt, ExamCertificate

logger = logging.getLogger(__name__)


@receiver(post_save, sender=ExamAttempt)
def auto_create_certificate_on_pass(sender, instance, created, update_fields, **kwargs):
    """
    Automatically create an ExamCertificate when an exam attempt is passed.
    
    This signal fires after an ExamAttempt is saved. If the attempt:
    - Is submitted (is_submitted=True)
    - Has passed (is_passed=True)
    - Has a score of 80% or above
    
    Then a certificate is automatically created with all student and exam details.
    """
    try:
        # Only process if this is a submitted and passed attempt with 80%+
        if not instance.is_submitted or not instance.is_passed:
            return
        
        if instance.score_percentage is None or instance.score_percentage < 80:
            return
        
        # Check if certificate already exists
        if ExamCertificate.objects.filter(exam_attempt=instance).exists():
            # Certificate already created, skip
            return
        
        # Get related objects
        user = instance.course_access.user
        course = instance.course_access.course
        payment = instance.course_access.payment
        
        # Calculate course duration in months
        course_duration_days = getattr(course, 'duration', 30)
        course_duration_months = round(float(course_duration_days) / 30, 2)
        
        # Get purchase and join dates
        purchased_date = payment.created_at if payment else instance.course_access.created_at
        joined_date = instance.course_access.created_at
        
        # Compile violation details
        violations = instance.violations.all()
        violation_details = []
        for violation in violations:
            violation_details.append({
                'type': violation.get_violation_type_display(),
                'count': violation.violation_count,
                'description': violation.description,
                'recorded_at': violation.recorded_at.isoformat() if violation.recorded_at else None,
            })
        
        # Create certificate
        certificate = ExamCertificate.objects.create(
            exam_attempt=instance,
            student_name=user.get_full_name() or user.username or user.email,
            student_email=user.email,
            student_phone=getattr(user, 'profile', {}).get('phone', '') if hasattr(user, 'profile') else '',
            course_name=course.name,
            course_duration_days=course_duration_days,
            course_duration_months=course_duration_months,
            purchased_date=purchased_date,
            joined_date=joined_date,
            exam_score_percentage=instance.score_percentage,
            correct_answers=instance.correct_answers,
            total_questions=instance.total_questions,
            exam_duration_taken_minutes=instance.time_taken_seconds // 60 if instance.time_taken_seconds else 0,
            exam_submitted_date=instance.submitted_at or timezone.now(),
            has_violations=instance.has_violations,
            violation_count=instance.violation_count,
            violation_details=json.dumps(violation_details) if violation_details else None,
            is_active=True,
        )
        
        logger.info(
            f'Certificate auto-created for {user.email} - {course.name} '
            f'(Score: {instance.score_percentage}%)'
        )
        
    except Exception as e:
        logger.error(f'Error auto-creating certificate: {str(e)}', exc_info=True)


# Optional: Add a signal to handle certificate file uploads
@receiver(post_save, sender=ExamCertificate)
def certificate_file_upload_notification(sender, instance, created, update_fields, **kwargs):
    """
    Optional: Send notification when certificate file is uploaded.
    Can be extended to send emails to users when their certificates are ready.
    """
    try:
        # Check if certificate_file was just uploaded
        if not created and update_fields and 'certificate_file' in update_fields:
            if instance.certificate_file:
                logger.info(
                    f'Certificate file uploaded for {instance.student_email} - {instance.course_name}'
                )
                # TODO: Send email to user notifying them certificate is ready
                # Example: send_certificate_ready_email(instance)
    except Exception as e:
        logger.error(f'Error in certificate upload notification: {str(e)}', exc_info=True)
