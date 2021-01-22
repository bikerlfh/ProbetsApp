import logging
from datetime import datetime
from django.core.management.base import BaseCommand
from apps.games.constants import GameStatus
from apps.data import services


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'create game data by advance analysis'

    def add_arguments(self, parser):
        parser.add_argument('--start_dt', type=str, help='game start dt')

    def handle(self, *args, **options):
        start_dt = options.get('start_dt')
        if start_dt:
            start_dt = datetime.strptime(start_dt, '%Y-%m-%d').date()
        services.create_game_data_by_advance_analysis(
            start_dt=start_dt,
            status=GameStatus.FINISHED.value
        )
        self.stdout.write(
            self.style.SUCCESS('command finished')
        )
