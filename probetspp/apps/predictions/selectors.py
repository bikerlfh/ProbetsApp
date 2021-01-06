from datetime import date
from typing import Optional, Union, List
from django.db.models import QuerySet

from apps.predictions.models import Prediction


def filter_prediction(
    *,
    game_id: Optional[int] = None,
    status: Optional[Union[List, int]] = None,
    league_id: Optional[int] = None,
    game_date: Optional[date] = None
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
    if game_date:
        filter_.update(game__start_dt__date=game_date)
    if filter_:
        prediction_qry = prediction_qry.filter(**filter_)
    return prediction_qry


def filter_prediction_by_game_id(
    *,
    game_id: int,
    status: Optional[Union[List, int]] = None
) -> 'QuerySet[Prediction]':
    return filter_prediction(
        game_id=game_id,
        status=status
    )
