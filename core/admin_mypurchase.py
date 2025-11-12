from django.contrib import admin
from .models_mypurchase import MyPurchaseSettings

@admin.register(MyPurchaseSettings)
class MyPurchaseSettingsAdmin(admin.ModelAdmin):
    """Admin interface for MyPurchaseSettings model."""
    list_display = ['__str__', 'is_active', 'updated_at']
    fieldsets = (
        ('Card Appearance', {
            'fields': (
                'background_color',
                'text_color',
                'card_shadow',
                'border_radius',
            )
        }),
        ('Button Settings', {
            'fields': (
                'button_background',
                'button_text_color',
                'button_text',
            )
        }),
        ('Progress Bar', {
            'fields': ('progress_bar_color',)
        }),
        ('Default Image', {
            'fields': ('default_image',)
        }),
        ('Status', {
            'fields': ('is_active',)
        })
    )