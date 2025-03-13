from django.apps import AppConfig
from django.db.models.signals import post_migrate


class SubscriberConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscriber'

    def ready(self):
        # Import signals here to register them properly
        from .signals import setup_periodic_tasks  # Import only when the app is fully loaded
        post_migrate.connect(setup_periodic_tasks, sender=self)
