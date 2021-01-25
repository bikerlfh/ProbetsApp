from os import getenv
from enum import IntEnum
from decimal import Decimal

LAST_H2H_GAMES_LIMIT_PREDICTION = int(getenv(
    'LAST_H2H_GAMES_LIMIT_PREDICTION', 5
))
ALLOWED_H2H_PERCENTAGE = Decimal(getenv(
    'ALLOWED_H2H_PERCENTAGE',
    66.6
))
NUM_H2H_GAMES_TO_PREDICT = int(getenv(
    'NUM_H2H_GAMES_TO_PREDICT', 3
))


ALLOWED_PERCENTAGE_LAST_GAMES = Decimal(getenv(
    'ALLOWED_PERCENTAGE_LAST_GAMES',
    66.6
))
NUM_LAST_GAMES_TO_PREDICT = int(getenv(
    'NUM_LAST_GAMES_TO_PREDICT', 10
))


class PredictionStatus(IntEnum):
    DEFAULT = 0
    WON = 1
    LOSE = 2
    CANCELED = -1
    ERROR_CORE = -2


class WinnerPrediction(IntEnum):
    NO_DATA = -1
    HOME_OR_AWAY = 0
    HOME_PLAYER = 1
    AWAY_PLAYER = 2
