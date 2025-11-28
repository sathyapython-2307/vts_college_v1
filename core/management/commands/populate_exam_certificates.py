"""
Management command to automatically populate ExamCertificate records
from ExamAttempt records where score >= 80%.

Usage:
    python manage.py populate_exam_certificates
    python manage.py populate_exam_certificates --course_id=1
    python manage.py populate_exam_certificates --recreate  # Delete and recreate all certificates
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from core.models import ExamAttempt, ExamCertificate, CourseAccess, CoursePayment
from decimal import Decimal
import json
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate ExamCertificate records from passing exam attempts (80%+)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--course_id',
            type=int,
            help='Process certificates only for a specific course ID',
        )
        parser.add_argument(
            '--recreate',
            action='store_true',
            help='Delete all existing certificates and recreate them (use with caution)',
        )
        parser.add_argument(
            '--user_id',
            type=int,
            help='Process certificates only for a specific user ID',
        )

    def handle(self, *args, **options):
        """Main command handler"""
        if options['recreate']:
            if self._confirm_recreate():
                self.stdout.write('Deleting all existing certificates...')
                ExamCertificate.objects.all().delete()
                self.stdout.write(self.style.SUCCESS('Certificates deleted.'))
            else:
                self.stdout.write(self.style.WARNING('Recreate cancelled.'))
                return

        # Build filter criteria
        filter_kwargs = {
            'is_submitted': True,
            'is_passed': True,
            'score_percentage__gte': Decimal('80'),
        }

        if options['course_id']:
            filter_kwargs['course_access__course_id'] = options['course_id']

        if options['user_id']:
            filter_kwargs['course_access__user_id'] = options['user_id']

        # Fetch all passing exam attempts
        passing_attempts = ExamAttempt.objects.filter(**filter_kwargs).select_related(
            'course_access__user',
            'course_access__course',
            'course_access__payment'
        ).prefetch_related('violations')

        self.stdout.write(f'Found {passing_attempts.count()} passing exam attempt(s)...')

        created_count = 0
        updated_count = 0
        skipped_count = 0

        with transaction.atomic():
            for attempt in passing_attempts:
                try:
                    certificate, created = self._create_or_update_certificate(attempt)
                    if created:
                        created_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(
                                f'✓ Created certificate for {attempt.course_access.user.email} '
                                f'({attempt.course_access.course.name} - {attempt.score_percentage}%)'
                            )
                        )
                    else:
                        updated_count += 1
                        self.stdout.write(
                            f'⟳ Updated certificate for {attempt.course_access.user.email}'
                        )
                except Exception as e:
                    skipped_count += 1
                    self.stdout.write(
                        self.style.ERROR(
                            f'✗ Error processing attempt {attempt.id}: {str(e)}'
                        )
                    )

        # Summary
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS(f'Created: {created_count}'))
        self.stdout.write(self.style.WARNING(f'Updated: {updated_count}'))
        self.stdout.write(self.style.ERROR(f'Skipped: {skipped_count}'))
        self.stdout.write('=' * 60)

    def _create_or_update_certificate(self, attempt):
        """Create or update an ExamCertificate from an ExamAttempt"""
        user = attempt.course_access.user
        course = attempt.course_access.course
        payment = attempt.course_access.payment

        # Calculate course duration in months
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
        certificate, created = ExamCertificate.objects.update_or_create(
            exam_attempt=attempt,
            defaults=data
        )

        return certificate, created

    def _confirm_recreate(self):
        """Ask for user confirmation before recreating certificates"""
        response = input(
            'WARNING: This will DELETE all existing exam certificates and recreate them. '
            'Continue? (yes/no): '
        )
        return response.lower() in ['yes', 'y']
