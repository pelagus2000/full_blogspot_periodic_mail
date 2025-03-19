from django.apps import AppConfig


class SignConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sign'

    def ready(self):
        try:
            import sign.signals
        except ImportError as e:
            raise ImportError(f"Error importing signals module: {e}")

