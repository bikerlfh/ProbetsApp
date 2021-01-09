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
    total_games = models.IntegerField(default=0)
    won_games = models.IntegerField(default=0)
    lost_games = models.IntegerField(default=0)
    won_sets = models.IntegerField(default=0)
    lost_sets = models.IntegerField(default=0)
    won_points = models.IntegerField(default=0)
    lost_points = models.IntegerField(default=0)
    back_to_win = models.IntegerField(default=0)
    back_to_lose = models.IntegerField(default=0)
    games_sold = models.IntegerField(default=0)
    total_predictions = models.IntegerField(default=0)
    won_predictions = models.IntegerField(default=0)
    lost_predictions = models.IntegerField(default=0)
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

    @property
    def h_id(self):
        return self.home_player_id

    @property
    def a_id(self):
        return self.away_player_id

    @property
    def winner_id(self):
        status = GameStatus(self.status)
        if status != GameStatus.FINISHED:
            return None
        if self.home_score > self.away_score:
            return self.h_id
        return self.a_id

    def __str__(self):
        return f'{self.home_player} vs {self.away_player}'

    def is_winner(self, player_id: int):
        return player_id == self.winner_id
