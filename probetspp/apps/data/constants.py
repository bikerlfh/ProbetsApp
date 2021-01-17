from os import getenv
from decimal import Decimal


MIN_DIFF_PLAYER_SCORE = int(getenv(
    'MIN_DIFF_PLAYER_SCORE', 80
))

MIN_TOTAL_GAMES_PLAYER = int(getenv(
    'MIN_TOTAL_GAMES_PLAYER', 10
))

DEFAULT_WEIGHTS = dict(
    WT_GAMES=Decimal(0.9),
    WT_SETS=Decimal(0.7),
    WT_POINTS=Decimal(0.5),
    WT_GAMES_SOLD=Decimal(0.8),
    WT_PREDICTIONS=Decimal(1)
)
