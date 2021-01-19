from os import getenv
from decimal import Decimal


MIN_DIFF_PLAYER_SCORE = int(getenv(
    'MIN_DIFF_PLAYER_SCORE', 120
))

MIN_TOTAL_GAMES_PLAYER = int(getenv(
    'MIN_TOTAL_GAMES_PLAYER', 10
))

DEFAULT_WEIGHTS = dict(
    wt_games=Decimal(0.9),
    wt_sets=Decimal(0.7),
    wt_points=Decimal(0.5),
    wt_games_sold=Decimal(0.8),
    wt_predictions=Decimal(1),
    wt_h2h=Decimal(1),
    wt_last_games=Decimal(0.8),
    wt_direct_opponents=Decimal(0.6)
)
