from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_coursescheduleitem_duration_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('progress_percentage', models.DecimalField(decimal_places=2, default=0.0, max_digits=5)),
                ('completed_lessons', models.JSONField(default=list)),
                ('is_completed', models.BooleanField(default=False)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
                ('last_accessed', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('course_access', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='progress', to='core.courseaccess')),
            ],
            options={
                'verbose_name': 'Course Progress',
                'verbose_name_plural': 'Course Progress',
            },
        ),
        migrations.CreateModel(
            name='Certificate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('certificate_type', models.CharField(choices=[('achievement', 'Certificate of Achievement'), ('participation', 'Statement of Participation')], max_length=20)),
                ('certificate_number', models.CharField(max_length=50, unique=True)),
                ('issue_date', models.DateTimeField(auto_now_add=True)),
                ('pdf_file', models.FileField(upload_to='certificates/')),
                ('course_progress', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='certificate', to='core.courseprogress')),
            ],
            options={
                'verbose_name': 'Certificate',
                'verbose_name_plural': 'Certificates',
            },
        ),
    ]