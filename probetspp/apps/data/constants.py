from os import getenv
from decimal import Decimal


MIN_NUM_H2H_GAMES_TO_PREDICT = int(getenv(
    'MIN_NUM_H2H_GAMES_TO_PREDICT', 10
))

MIN_NUM_LAST_GAMES_TO_PREDICT = int(getenv(
    'MIN_NUM_LAST_GAMES_TO_PREDICT', 10
))


DEFAULT_WEIGHTS = dict(
    WT_GAMES=Decimal(0.9),
    WT_SETS=Decimal(0.7),
    WT_POINTS=Decimal(0.5),
    WT_GAMES_SOLD=Decimal(0.8),
    WT_PREDICTIONS=Decimal(1)
)
