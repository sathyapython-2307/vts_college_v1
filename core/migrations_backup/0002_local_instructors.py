"""Auto migration: add CourseLocalInstructor and remove old Course fields.

Generated manually to reflect model changes made to core.models.Course and
to introduce CourseLocalInstructor for per-course manual instructor entries.
"""
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseLocalInstructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_instructor_images/')),
                ('order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('is_primary', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='local_instructors', to='core.course')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Course Local Instructor',
                'verbose_name_plural': 'Course Local Instructors',
            },
        ),
        migrations.RemoveField(
            model_name='course',
            name='detailed_description',
        ),
        migrations.RemoveField(
            model_name='course',
            name='image',
        ),
        migrations.RemoveField(
            model_name='course',
            name='duration',
        ),
    ]
