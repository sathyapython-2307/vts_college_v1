"""
Django AppConfig for the core application.
Handles application initialization and signal registration.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuration for the core application."""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    verbose_name = 'VTS Core'
    
    def ready(self):
        """
        Import signals when app is ready.
        This ensures signal handlers are registered.
        """
        try:
            import core.signals  # noqa
        except ImportError:
            pass
