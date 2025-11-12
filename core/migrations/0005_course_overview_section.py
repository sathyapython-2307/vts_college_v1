from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0004_coursefeature'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseOverview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='course_overview_images/')),
                ('order', models.IntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('course', models.ForeignKey(on_delete=models.deletion.CASCADE, related_name='overviews', to='core.course')),
            ],
            options={
                'ordering': ['order'],
                'verbose_name': 'Course Overview',
                'verbose_name_plural': 'Course Overviews',
            },
        ),
    ]
