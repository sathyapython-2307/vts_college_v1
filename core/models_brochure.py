from django.db import models
from django.contrib.auth.models import User

class BrochureDownload(models.Model):
    """Track brochure downloads and user information."""
    user_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='brochure_downloads')
    brochure = models.ForeignKey('CourseBrochure', on_delete=models.CASCADE, related_name='downloads')
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    downloaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Brochure Download"
        verbose_name_plural = "Brochure Downloads"
        ordering = ['-downloaded_at']

    def __str__(self):
        return f"{self.user_name} - {self.course.name} - {self.downloaded_at}"