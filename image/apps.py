from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "image"

    def ready(self):
        """Connects signal handlers decorated with @receiver"""
        from image import signals  # noqa: F401
