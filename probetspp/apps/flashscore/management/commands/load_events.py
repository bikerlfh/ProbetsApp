from datetime import date, timedelta, datetime
from django.core.management.base import BaseCommand
from apps.flashscore import services


class Command(BaseCommand):
    help = 'Load events'
    date_format = '%Y-%m-%d'

    def add_arguments(self, parser):
        parser.add_argument('--file_date', type=str, help='file date')
        parser.add_argument(
            '--file_date_from',
            type=str,
            help='file date from',
        )
        parser.add_argument(
            '--file_date_to',
            type=str,
            help='file date from',
        )

    def load_events_date(self, file_date: date):
        self.stdout.write(
            self.style.SUCCESS(f'loading events from {file_date}....')
        )
        data = services.load_events(file_date=file_date)
        self.stdout.write(
            self.style.SUCCESS(data)
        )

    def handle(self, *args, **options):
        file_date = options['file_date']
        file_date_from = options['file_date_from']
        file_date_to = options['file_date_to']
        if file_date:
            self.stdout.write(
                self.style.SUCCESS(f'loading events from {file_date}....')
            )
            file_date = datetime.strptime(file_date, self.date_format)
            data = services.load_events(file_date=file_date)
            self.stdout.write(
                self.style.SUCCESS(data)
            )
        elif file_date_from:
            file_date = datetime.strptime(
                file_date_from,
                self.date_format
            ).date()
            file_date_to_ = date.today()
            if file_date_to:
                file_date_to_ = datetime.strptime(
                    file_date_to,
                    self.date_format
                )
            self.stdout.write(
                self.style.SUCCESS(
                    f'loading all events from {file_date} '
                    f'to {file_date_to_}....'
                )
            )
            while True:
                self.load_events_date(file_date=file_date)
                file_date += timedelta(days=1)
                if file_date > file_date_to_:
                    break
        else:
            self.stdout.write(
                self.style.SUCCESS('loading today events....')
            )
            data = services.load_events()
            self.stdout.write(
                self.style.SUCCESS(data)
            )
        self.stdout.write(
            self.style.SUCCESS('command ended')
        )
