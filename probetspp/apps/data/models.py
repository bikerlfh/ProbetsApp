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
    wt_h2h = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )
    wt_last_games = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )
    wt_direct_opponents = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10
    )


class AcceptanceValue(BaseModel):
    """
    save acceptance values
    to predict a game
    """
    p_wt_diff = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='min player wt diff'
    )
    h2h_wt_diff = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='min h2h wt diff'
    )
    l_g_wt_diff = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='min last games wt diff'
    )
    d_opp_wt_diff = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='min direct opponents wt diff'
    )
    is_active = models.BooleanField(
        default=True
    )


class DataGame(BaseModel):
    game = models.OneToOneField(
        Game,
        on_delete=models.DO_NOTHING,
        related_name='data'
    )
    acceptance_value = models.ForeignKey(
        AcceptanceValue,
        on_delete=models.DO_NOTHING,
        related_name='data_games'
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
    h_h2h_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='away h2h wt score'
    )
    a_h2h_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='away h2h wt score'
    )
    h_l_g_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='home last games wt score'
    )
    a_l_g_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='away last games wt score'
    )
    h_d_opp_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='home direct opponents wt score'
    )
    a_d_opp_wt_score = models.DecimalField(
        default=Decimal(0),
        max_digits=18,
        decimal_places=10,
        verbose_name='away direct opponents wt score'
    )
