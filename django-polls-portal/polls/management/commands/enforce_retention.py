from django.core.management.base import BaseCommand

from polls.services.retention import enforce_retention


class Command(BaseCommand):
    help = "Delete or anonymize expired poll response/review records"

    def handle(self, *args, **options):
        results = enforce_retention()
        self.stdout.write(self.style.SUCCESS(f"retention cleanup complete: {results}"))
