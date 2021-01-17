import logging
import json
from django.db import transaction
from django.core.serializers.json import DjangoJSONEncoder
from datetime import datetime, date
from typing import Dict, Any, List, Optional, Union
from rest_framework.exceptions import ValidationError

from apps.data.weights import wt_score
from apps.games.models import Game
from apps.games.constants import GameStatus
from apps.games import (
    selectors as games_selectors,
    services as games_services
)

from apps.predictions.prediction import BasicPrediction
from apps.predictions.constants import (
    WinnerPrediction,
    PredictionStatus
)
from apps.predictions.models import Prediction
from apps.predictions import selectors

logger = logging.getLogger(__name__)


def get_prediction_data_today(
    *,
    league_id: Optional[int] = None,
    game_date: Optional[date] = None
) -> List[Dict[str, Any]]:
    if not game_date:
        now = datetime.now().date()
        game_date = now
    games_qry = games_selectors.filter_games(
        status=GameStatus.SCHEDULED.value,
        start_dt=game_date,
        league_id=league_id
    )
    predictions_data = []
    for game in games_qry:
        game_data = games_services.\
            get_game_data_to_prediction(game=game)
        basic_prediction = BasicPrediction(
            game_data=game_data
        )
        prediction = basic_prediction.get_prediction()
        if prediction:
            predictions_data.append(prediction)
    logger.info(
        f'get_prediction_data_today :: total '
        f'predictions: {len(predictions_data)}'
    )
    return predictions_data


def create_prediction(
    *,
    game_id: int,
    player_winner_id: int,
    status: Optional[int] = None,
    game_data: Optional[Dict[str, Any]] = None
) -> Union[None]:
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
        logger.error(
            f'create_prediction :: {msg}'
        )
        raise ValidationError(msg)

    if game.home_player != player_winner and \
            game.away_player != player_winner:
        msg = f'player {player_winner_id} ' \
              f'not in game {game_id}'
        logger.error(
            f'create_prediction :: {msg}'
        )
        raise ValidationError(msg)
    Prediction.objects.create(
        game=game,
        player_winner=player_winner,
        status=status,
        game_data=json.dumps(game_data, cls=DjangoJSONEncoder)
    )


def create_predictions(
    *,
    league_id: Optional[int] = None,
    game_date: Optional[date] = None
) -> Dict[str, Any]:
    predictions_data = get_prediction_data_today(
        league_id=league_id,
        game_date=game_date
    )
    num_created = 0
    for data in predictions_data:
        game_id = data['id']
        winner_prediction = WinnerPrediction(data['winner_prediction'])
        home_player = data['home_player']
        away_player = data['away_player']
        player_winner_id = home_player['id']
        if winner_prediction == WinnerPrediction.AWAY_PLAYER:
            player_winner_id = away_player['id']
        prediction = selectors.filter_prediction_by_game_id(
            game_id=game_id,
        )
        if not prediction.exists():
            create_prediction(
                game_id=game_id,
                player_winner_id=player_winner_id,
                game_data=data
            )
            num_created += 1
            continue

    data = dict(
        predictions_created=num_created
    )
    return data


@transaction.atomic()
def create_predictions_by_wt_player_score(
    *,
    start_dt: Optional[date] = None
) -> int:
    """
    create predictions by wt player score
    Attrs:
        start_dt: game start date
    Return: num predictions created
    """
    wt_data = wt_score.\
        get_games_prediction_by_wt_score_player(
            start_dt=start_dt,
            create_data_game=True
        )
    for wt in wt_data:
        game_id = wt['id']
        winner_id = wt['winner_id_pdt']
        create_prediction(
            game_id=game_id,
            player_winner_id=winner_id,
            game_data=wt
        )
    return len(wt_data)


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
    if status == GameStatus.CANCELED:
        prediction.status = PredictionStatus.CANCELED.value
        prediction.save()
        return
    if status != GameStatus.FINISHED:
        return

    player_stats = games_selectors. \
        get_player_stats_by_player_id(
            player_id=prediction.player_winner_id
        )
    is_winner = game.is_winner(
        player_id=prediction.player_winner_id
    )
    player_stats.total_predictions += 1
    if is_winner:
        status = PredictionStatus.WON.value
        player_stats.won_predictions += 1
    else:
        status = PredictionStatus.LOSE.value
        player_stats.lost_predictions += 1
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
