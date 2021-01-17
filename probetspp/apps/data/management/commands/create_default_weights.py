from typing import Optional, Union
from django.core.management.base import BaseCommand

from apps.data.constants import DEFAULT_WEIGHTS
from apps.data import selectors, services


class Command(BaseCommand):
    help = 'create general weights'

    def add_arguments(self, parser):
        parser.add_argument('--player_id', type=int, help='player id')

    def create_default_weights(
        self,
        player_id: Optional[int] = None
    ) -> Union[None]:
        """
        create a default weights to player or general
        """
        data = dict(
            wt_games=DEFAULT_WEIGHTS['WT_GAMES'],
            wt_sets=DEFAULT_WEIGHTS['WT_SETS'],
            wt_points=DEFAULT_WEIGHTS['WT_POINTS'],
            wt_games_sold=DEFAULT_WEIGHTS['WT_GAMES_SOLD'],
            wt_predictions=DEFAULT_WEIGHTS['WT_PREDICTIONS'],
            player_id=player_id
        )
        default_wt_qry = selectors. \
            filter_default_data_weights()
        if default_wt_qry.exists() and not player_id:
            if not player_id:
                return
            default_ = default_wt_qry.first()[0]
            default_.pop('player_id')
            default_.pop('id')
            data.update(**default_)
        data = services.create_or_update_data_weights(**data)

    def handle(self, *args, **options):
        player_id = options.get('player_id')
        self.create_default_weights(
            player_id=player_id
        )
        self.stdout.write(
            self.style.SUCCESS('command finished')
        )
