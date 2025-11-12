from django.db import models
from django.core.validators import MinValueValidator

class MyPurchaseSettings(models.Model):
    """Settings for the My Purchase page course cards."""
    background_color = models.CharField(max_length=50, default='#ffffff', help_text='Card background color (hex)')
    text_color = models.CharField(max_length=50, default='#333333', help_text='Card text color (hex)')
    button_background = models.CharField(max_length=50, default='#28a745', help_text='Button background color (hex)')
    button_text_color = models.CharField(max_length=50, default='#ffffff', help_text='Button text color (hex)')
    button_text = models.CharField(max_length=50, default='Start Learning', help_text='Text for the button')
    card_shadow = models.CharField(max_length=100, default='0 4px 6px rgba(0, 0, 0, 0.1)', help_text='CSS box-shadow value')
    border_radius = models.CharField(max_length=20, default='15px', help_text='Card border radius')
    progress_bar_color = models.CharField(max_length=50, default='#28a745', help_text='Progress bar color (hex)')
    default_image = models.ImageField(
        upload_to='course_placeholder/',
        null=True, blank=True,
        help_text='Default image for courses without their own image'
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "My Purchase Page Settings"
        verbose_name_plural = "My Purchase Page Settings"

    def __str__(self):
        return "My Purchase Page Settings"