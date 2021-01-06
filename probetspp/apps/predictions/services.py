import logging
import json
from django.core.serializers.json import DjangoJSONEncoder

from datetime import datetime, date
from typing import Dict, Any, List, Optional, Union
from rest_framework.exceptions import ValidationError

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


def update_prediction_by_game_updated(
    *,
    game: Game
) -> Union[None]:
    prediction = selectors.filter_prediction_by_game_id(
        game_id=game.id,
        status=PredictionStatus.DEFAULT.value
    )
    if not prediction.exists():
        return
    prediction = prediction.first()
    game_status = GameStatus(game.status)
    if game_status == GameStatus.CANCELED:
        prediction.status = PredictionStatus.CANCELED.value
        prediction.save()
        return
    if game_status != GameStatus.FINISHED:
        return
    is_winner = game.is_winner(
        player_id=prediction.player_winner_id
    )
    status = PredictionStatus.WON.value
    if not is_winner:
        status = PredictionStatus.LOSE.value
    prediction.status = status
    prediction.save()

