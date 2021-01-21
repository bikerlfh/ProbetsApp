from decimal import Decimal


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
