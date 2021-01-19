from django.core.management.base import BaseCommand
from apps.data import services


class Command(BaseCommand):
    help = 'create general weights'

    def add_arguments(self, parser):
        parser.add_argument('--player_id', type=int, help='player id')

    def handle(self, *args, **options):
        player_id = options.get('player_id')
        services.create_default_weights(
            player_id=player_id
        )
        self.stdout.write(
            self.style.SUCCESS('command finished')
        )
