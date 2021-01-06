from decimal import Decimal
from django.db import models

from apps.core.models import BaseModel
from apps.core.constants import GenderConstants
from apps.games.constants import GameStatus


class Player(BaseModel):
    external_id = models.CharField(
        null=False,
        max_length=50,
        unique=True
    )
    short_name = models.CharField(
        null=True,
        max_length=15
    )
    name = models.CharField(
        null=False,
        max_length=150
    )
    gender = models.SmallIntegerField(
        default=GenderConstants.MALE.value
    )

    def __str__(self):
        return self.name


class PlayerStats(BaseModel):
    player = models.OneToOneField(
        Player,
        on_delete=models.DO_NOTHING,
        related_name='stats'
    )
    total_games = models.IntegerField(
        default=0
    )
    won_games = models.IntegerField(
        default=0
    )
    lost_games = models.IntegerField(
        default=0
    )
    prediction_games = models.IntegerField(
        default=0
    )
    confidence_percentage = models.DecimalField(
        default=Decimal(0),
        max_digits=5,
        decimal_places=2
    )


class League(BaseModel):
    external_id = models.CharField(
        null=False,
        max_length=50
    )
    gender = models.SmallIntegerField(
        default=GenderConstants.MALE.value
    )
    name = models.CharField(
        null=False,
        max_length=150
    )

    class Meta:
        unique_together = ('external_id', 'gender',)

    def __str__(self):
        gender = GenderConstants(self.gender)
        if gender == GenderConstants.FEMALE:
            return f'{GenderConstants(self.gender).name} ' \
                   f'- {self.name}'
        return self.name


class Game(BaseModel):
    external_id = models.CharField(
        null=False,
        max_length=150,
        unique=True
    )
    league = models.ForeignKey(
        League,
        on_delete=models.DO_NOTHING,
        related_name='home_visitor',
        null=False
    )
    home_player = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        related_name='home_games',
        null=False
    )
    away_player = models.ForeignKey(
        Player,
        on_delete=models.DO_NOTHING,
        related_name='away_games',
        null=False
    )
    start_dt = models.DateTimeField()
    status = models.SmallIntegerField(
        default=GameStatus.DEFAULT.value
    )
    home_score = models.SmallIntegerField(default=0)
    away_score = models.SmallIntegerField(default=0)
    line_score = models.JSONField(null=True)

    def is_winner(self, player_id: int):
        status = GameStatus(self.status)
        if status != GameStatus.FINISHED:
            return None
        if self.home_score > self.away_score:
            return self.home_player_id == player_id
        return self.away_player_id == player_id
