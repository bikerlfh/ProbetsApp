import logging
import json
from decimal import Decimal
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Union

from apps.data import services as data_services
from apps.games.models import Game
from apps.games.constants import GameStatus
from apps.games import selectors as games_selectors

from apps.predictions.constants import PredictionStatus
from apps.predictions.models import Prediction
from apps.predictions import selectors

logger = logging.getLogger(__name__)


def create_prediction(
    *,
    game_id: int,
    player_winner_id: int,
    confidence: Decimal,
    status: Optional[int] = None,
    game_data: Optional[Dict[str, Any]] = None
) -> Union[Dict[str, Any], None]:
    game = games_selectors.\
        filter_game_by_id(game_id=game_id).first()
    player_winner = games_selectors.filter_player_by_id(
        player_id=player_winner_id
    ).first()
    if not status:
        status = PredictionStatus.DEFAULT.value

    prediction_qry = selectors.filter_prediction(
        game_id=game_id
    )
    if prediction_qry.exists():
        msg = f'prediction for game {game_id} already exists'
        logger.warning(f'create_prediction :: {msg}')
        return

    if game.home_player != player_winner and \
            game.away_player != player_winner:
        msg = f'player {player_winner_id} ' \
              f'not in game {game_id}'
        logger.error(f'create_prediction :: {msg}')
        return
    data = dict(
        game=game,
        player_winner=player_winner,
        status=status,
        confidence=confidence
    )
    if game_data:
        data.update(
            game_data=json.dumps(game_data, cls=DjangoJSONEncoder)
        )
    prediction = Prediction.objects.create(**data)
    winner = prediction.player_winner
    data_ = dict(
        game=str(game),
        league=str(game.league),
        start_dt=game.start_dt,
        winner=str(winner),
        confidence=confidence,
        odds=game.player_odds(player_id=winner.id)
    )
    return data_


def create_prediction_by_advance_analysis(
    *,
    game_id: Optional[int] = None,
    status: Optional[int] = None,
    start_dt: Optional[date] = None,
    start_dt_range: Optional[List[datetime]] = None
) -> List[Dict[str, Any]]:
    if not status:
        status = GameStatus.SCHEDULED.value
    if not start_dt:
        start_dt = datetime.now().date()
    predictions_data = data_services.\
        get_games_data_to_predict_by_advance_analysis(
            game_id=game_id,
            status=status,
            start_dt=start_dt,
            start_dt_range=start_dt_range
        )
    predictions = []
    for data in predictions_data:
        prediction = create_prediction(
            game_id=data['game_id'],
            player_winner_id=data['winner_id'],
            confidence=data['confidence']
        )
        if not prediction:
            continue
        predictions.append(prediction)
    return predictions


@transaction.atomic()
def update_prediction_by_game_updated(
    *,
    game: Game
) -> Union[None]:
    """
    update prediction and player stats (prediction)
    from game update
    Attrs:
        game: Game object
    Returns: None
    """
    prediction = selectors.filter_prediction_by_game_id(
        game_id=game.id,
        status=PredictionStatus.DEFAULT.value
    )
    if not prediction.exists():
        return
    prediction = prediction.first()
    status = GameStatus(game.status)
    if status == GameStatus.CANCELED or status == GameStatus.ABANDONMENT:
        prediction.status = PredictionStatus.CANCELED.value
        prediction.save()
        return
    if status != GameStatus.FINISHED:
        return

    h_id = game.h_id
    a_id = game.a_id
    pdt_winner_id = prediction.player_winner_id
    # when player has been changed
    if h_id != pdt_winner_id and a_id != pdt_winner_id:
        prediction.status = PredictionStatus.ERROR_CORE.value
        prediction.save()
        return

    player_stats = games_selectors. \
        get_player_stats_by_player_id(
            player_id=prediction.player_winner_id
        )
    is_winner = game.is_winner(
        player_id=pdt_winner_id
    )
    player_stats.total_predictions += 1
    if is_winner:
        status = PredictionStatus.WON.value
        player_stats.won_predictions += 1
    else:
        status = PredictionStatus.LOSE.value
        player_stats.lost_predictions += 1
        if prediction.confidence == 100:
            player_stats.games_sold += 1
    c_percentage = 100 * (player_stats.won_predictions
                          / player_stats.total_predictions)
    player_stats.confidence_percentage = c_percentage
    player_stats.save()
    prediction.status = status
    prediction.save()


def recalculate_prediction_stats(
    *,
    player_id: int
) -> Union[None]:
    prediction_qry = selectors.\
        filter_prediction_by_player_winner_id(
            player_id=player_id
        )
    if not prediction_qry.exists():
        return
    player_stats = games_selectors. \
        get_player_stats_by_player_id(player_id=player_id)
    t_prediction = 0
    w_prediction = 0
    l_prediction = 0

    for data in prediction_qry:
        t_prediction += 1
        status = PredictionStatus(data.status)
        if status == PredictionStatus.WON:
            w_prediction += 1
            continue
        l_prediction += 1
    player_stats.total_predictions = t_prediction
    player_stats.won_predictions = w_prediction
    player_stats.lost_predictions = l_prediction
    c_percentage = 100 * (w_prediction / t_prediction)
    player_stats.confidence_percentage = c_percentage
    player_stats.save()
