from decimal import Decimal
from django.db import models

from apps.core.models import BaseModel

from apps.games.models import Player, Game


class DataWeights(BaseModel):
    """
    save the data weights.
    if player is null, the weights
    object must be apply to all player without weights
    """
    player = models.OneToOneField(
        Player,
        on_delete=models.DO_NOTHING,
        related_name='data_profile',
        null=True,
        unique=True
    )
    wt_games = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )
    wt_sets = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )
    wt_points = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )
    wt_games_sold = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )
    wt_predictions = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )


class DataGame(BaseModel):
    game = models.OneToOneField(
        Game,
        on_delete=models.DO_NOTHING,
        related_name='data'
    )
    h_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='home wt score'
    )
    a_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='away wt score'
    )
