from django.core.management.base import BaseCommand
from subscriber.tasks import weekly_newsletter


class Command(BaseCommand):
    help = "Send the weekly newsletter immediately."

    def handle(self, *args, **kwargs):
        self.stdout.write("Sending weekly newsletter...")
        weekly_newsletter.delay()  # Triggers the Celery task asynchronously
        self.stdout.write("Weekly newsletter task has been triggered.")
