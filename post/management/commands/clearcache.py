from django.core.cache import cache
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Clears the entire cache"

    def handle(self, *args, **options):
        self.stdout.write("Clearing cache...")
        cache.clear()
        self.stdout.write("Cache cleared.")
