from django.core.management.base import BaseCommand
from apps.predictions import tasks


class Command(BaseCommand):
    help = 'create periodical predictions'

    def handle(self, *args, **options):
        tasks.create_periodical_prediction()
        self.stdout.write(
            self.style.SUCCESS('command ended')
        )
