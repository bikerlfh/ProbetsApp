from datetime import date
from typing import Optional, Union, List
from django.db.models import QuerySet

from apps.predictions.models import Prediction
from apps.predictions.constants import PredictionStatus


def filter_prediction(
    *,
    game_id: Optional[int] = None,
    status: Optional[Union[List, int]] = None,
    league_id: Optional[int] = None,
    start_dt: Optional[date] = None
) -> 'QuerySet[Prediction]':
    filter_ = dict()
    prediction_qry = Prediction.objects.all()
    if game_id:
        filter_.update(game_id=game_id)
    if isinstance(status, list):
        filter_.update(status__in=status)
    elif isinstance(status, int):
        filter_.update(status=status)
    if league_id:
        filter_.update(game__league_id=league_id)
    if start_dt:
        filter_.update(game__start_dt__date=start_dt)
    if filter_:
        prediction_qry = prediction_qry.filter(**filter_)
    return prediction_qry.order_by('game__start_dt')


def filter_prediction_by_game_id(
    *,
    game_id: int,
    status: Optional[Union[List, int]] = None
) -> 'QuerySet[Prediction]':
    return filter_prediction(
        game_id=game_id,
        status=status
    )


def filter_prediction_by_player_winner_id(
    *,
    player_id: int
) -> 'QuerySet[Prediction]':
    return filter_prediction(
        status=[
            PredictionStatus.WON.value,
            PredictionStatus.LOSE.value
        ]
    ).filter(player_winner_id=player_id)
