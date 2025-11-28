"""
Certificate utility functions for exam certificate management.
Provides helper functions for creating, updating, and querying certificates.
"""

from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import ExamAttempt, ExamCertificate, CoursePayment
import json
from datetime import timedelta


def get_passing_attempts(min_score=80, course_id=None, user_id=None):
    """
    Fetch exam attempts that meet passing criteria (default 80%+).
    
    Args:
        min_score: Minimum percentage score to qualify
        course_id: Optional filter by course ID
        user_id: Optional filter by user ID
    
    Returns:
        QuerySet of passing ExamAttempt objects
    """
    filter_kwargs = {
        'is_submitted': True,
        'is_passed': True,
        'score_percentage__gte': Decimal(str(min_score)),
    }
    
    if course_id:
        filter_kwargs['course_access__course_id'] = course_id
    
    if user_id:
        filter_kwargs['course_access__user_id'] = user_id
    
    return ExamAttempt.objects.filter(**filter_kwargs).select_related(
        'course_access__user',
        'course_access__course',
        'course_access__payment'
    ).prefetch_related('violations')


def create_certificate_from_attempt(attempt, force_update=False):
    """
    Create or update an ExamCertificate from a passing ExamAttempt.
    
    Args:
        attempt: ExamAttempt instance
        force_update: If True, always update even if certificate exists
    
    Returns:
        Tuple of (certificate, created) where created is boolean
    
    Raises:
        ValueError: If attempt doesn't meet passing criteria
    """
    if attempt.score_percentage < Decimal('80'):
        raise ValueError(f"Attempt score {attempt.score_percentage}% is below 80% threshold")
    
    if not attempt.is_submitted or not attempt.is_passed:
        raise ValueError("Attempt must be submitted and passed")
    
    user = attempt.course_access.user
    course = attempt.course_access.course
    payment = attempt.course_access.payment
    
    # Calculate course duration in months (default 30 days per month)
    course_duration_days = getattr(course, 'duration', 30)
    course_duration_months = round(Decimal(course_duration_days) / Decimal(30), 2)
    
    # Get purchase and join dates
    purchased_date = payment.created_at if payment else attempt.course_access.created_at
    joined_date = attempt.course_access.created_at
    
    # Compile violation details
    violations = attempt.violations.all()
    violation_details = []
    for violation in violations:
        violation_details.append({
            'type': violation.get_violation_type_display(),
            'count': violation.violation_count,
            'description': violation.description,
            'recorded_at': violation.recorded_at.isoformat() if violation.recorded_at else None,
        })
    
    # Prepare data
    data = {
        'student_name': user.get_full_name() or user.username or user.email,
        'student_email': user.email,
        'student_phone': getattr(user, 'profile', {}).get('phone', '') if hasattr(user, 'profile') else '',
        'course_name': course.name,
        'course_duration_days': course_duration_days,
        'course_duration_months': course_duration_months,
        'purchased_date': purchased_date,
        'joined_date': joined_date,
        'exam_score_percentage': attempt.score_percentage,
        'correct_answers': attempt.correct_answers,
        'total_questions': attempt.total_questions,
        'exam_duration_taken_minutes': attempt.time_taken_seconds // 60 if attempt.time_taken_seconds else 0,
        'exam_submitted_date': attempt.submitted_at or timezone.now(),
        'has_violations': attempt.has_violations,
        'violation_count': attempt.violation_count,
        'violation_details': json.dumps(violation_details) if violation_details else None,
    }
    
    # Create or update certificate
    if force_update:
        certificate, created = ExamCertificate.objects.update_or_create(
            exam_attempt=attempt,
            defaults=data
        )
    else:
        certificate, created = ExamCertificate.objects.get_or_create(
            exam_attempt=attempt,
            defaults=data
        )
    
    return certificate, created


def bulk_create_certificates(attempts):
    """
    Create certificates for multiple passing attempts.
    
    Args:
        attempts: QuerySet or list of ExamAttempt objects
    
    Returns:
        Dictionary with keys 'created', 'updated', 'skipped'
    """
    stats = {
        'created': 0,
        'updated': 0,
        'skipped': 0,
        'errors': []
    }
    
    with transaction.atomic():
        for attempt in attempts:
            try:
                cert, created = create_certificate_from_attempt(attempt)
                if created:
                    stats['created'] += 1
                else:
                    stats['updated'] += 1
            except Exception as e:
                stats['skipped'] += 1
                stats['errors'].append({
                    'attempt_id': attempt.id,
                    'error': str(e)
                })
    
    return stats


def get_student_certificates(user):
    """
    Get all exam certificates for a specific user.
    
    Args:
        user: Django User instance
    
    Returns:
        QuerySet of ExamCertificate objects for the user
    """
    return ExamCertificate.objects.filter(
        exam_attempt__course_access__user=user,
        is_active=True
    ).select_related(
        'exam_attempt__course_access__course'
    ).order_by('-exam_submitted_date')


def get_certificate_stats():
    """
    Get overall statistics about exam certificates.
    
    Returns:
        Dictionary with certificate statistics
    """
    total = ExamCertificate.objects.count()
    with_file = ExamCertificate.objects.exclude(certificate_file='').count()
    without_file = total - with_file
    with_violations = ExamCertificate.objects.filter(has_violations=True).count()
    
    # Average score
    from django.db.models import Avg
    avg_score = ExamCertificate.objects.aggregate(Avg('exam_score_percentage'))['exam_score_percentage__avg'] or 0
    
    return {
        'total_certificates': total,
        'certificates_with_file': with_file,
        'certificates_without_file': without_file,
        'with_violations': with_violations,
        'average_score': round(float(avg_score), 2),
    }


def search_certificates(query, search_fields=None):
    """
    Search certificates by student name, email, or course name.
    
    Args:
        query: Search string
        search_fields: List of fields to search in
    
    Returns:
        QuerySet of matching ExamCertificate objects
    """
    if search_fields is None:
        search_fields = ['student_name', 'student_email', 'course_name']
    
    from django.db.models import Q
    
    q_objects = Q()
    for field in search_fields:
        q_objects |= Q(**{f'{field}__icontains': query})
    
    return ExamCertificate.objects.filter(q_objects).order_by('-exam_submitted_date')


def export_certificates_to_excel(certificates, include_violations=True):
    """
    Prepare certificate data for Excel export.
    
    Args:
        certificates: QuerySet or list of ExamCertificate objects
        include_violations: Whether to include violation details
    
    Returns:
        List of dictionaries suitable for DataFrame creation
    """
    data = []
    
    for cert in certificates:
        row = {
            'Student Name': cert.student_name,
            'Email': cert.student_email,
            'Phone': cert.student_phone or 'N/A',
            'Course Name': cert.course_name,
            'Course Duration (Days)': cert.course_duration_days,
            'Course Duration (Months)': cert.course_duration_months,
            'Purchased Date': cert.purchased_date.strftime('%Y-%m-%d %H:%M:%S') if cert.purchased_date else '',
            'Joined Date': cert.joined_date.strftime('%Y-%m-%d %H:%M:%S') if cert.joined_date else '',
            'Exam Score (%)': cert.exam_score_percentage,
            'Correct Answers': cert.correct_answers,
            'Total Questions': cert.total_questions,
            'Exam Duration (Minutes)': cert.exam_duration_taken_minutes,
            'Exam Submitted Date': cert.exam_submitted_date.strftime('%Y-%m-%d %H:%M:%S') if cert.exam_submitted_date else '',
            'Certificate Status': 'Uploaded' if cert.certificate_file else 'Pending',
        }
        
        if include_violations:
            violations = cert.get_violation_list()
            violation_summary = ', '.join([v.get('type', 'Unknown') for v in violations]) if violations else 'None'
            row['Has Violations'] = 'Yes' if cert.has_violations else 'No'
            row['Violation Count'] = cert.violation_count
            row['Violation Details'] = violation_summary
        
        if cert.admin_notes:
            row['Admin Notes'] = cert.admin_notes
        
        data.append(row)
    
    return data
