from django.db import models

from apps.core.models import BaseModel

from apps.games.models import Game, Player
from apps.predictions.constants import PredictionStatus


class Prediction(BaseModel):
    external_id = models.CharField(
        null=True,
        max_length=50
    )
    game = models.ForeignKey(
        Game,
        on_delete=models.DO_NOTHING,
        related_name='predictions'
    )
    player_winner = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        related_name='prediction_winner'
    )
    status = models.SmallIntegerField(
        default=PredictionStatus.DEFAULT.value
    )
    game_data = models.JSONField(null=True)
    winner_prediction = models

    def __str__(self):
        return f'{self.game} ({self.player_winner})'

