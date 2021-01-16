import logging
from decimal import Decimal
from typing import Optional, Union

from apps.games import selectors as games_selectors
from apps.data.models import DataWeights
from apps.data.constants import DEFAULT_WEIGHTS
from apps.data.weights import selectors

logger = logging.getLogger(__name__)


def create_weights(
    *,
    wt_games: Decimal,
    wt_sets: Decimal,
    wt_points: Decimal,
    wt_games_sold: Decimal,
    wt_predictions: Decimal,
    player_id: Optional[int] = None,
) -> DataWeights:
    weight = DataWeights.objects.create(
        player_id=player_id,
        wt_games=wt_games,
        wt_sets=wt_sets,
        wt_points=wt_points,
        wt_games_sold=wt_games_sold,
        wt_predictions=wt_predictions
    )
    logger.info('data weight created')
    return weight


def create_or_update_data_weights(
    *,
    wt_games: Decimal,
    wt_sets: Decimal,
    wt_points: Decimal,
    wt_games_sold: Decimal,
    wt_predictions: Decimal,
    player_id: Optional[int] = None
) -> Union[DataWeights, None]:
    data = dict(
        wt_games=wt_games,
        wt_sets=wt_sets,
        wt_points=wt_points,
        wt_games_sold=wt_games_sold,
        wt_predictions=wt_predictions,
        player_id=player_id
    )
    if player_id:
        player_qry = games_selectors.filter_player_by_id(
            player_id=player_id
        )
        if not player_qry.exists():
            logger.error(
                f'create_or_update_data_weights :: '
                f'player {player_id} does not exists'
            )
            return
        weights_qry = selectors.\
            filter_data_weights_by_player_id(
                player_id=player_id
            )
    else:
        weights_qry = selectors. \
            filter_default_data_weights()

    if not weights_qry.exists():
        return create_weights(**data)
    weights_qry.update(
        wt_games=wt_games,
        wt_sets=wt_sets,
        wt_points=wt_points,
        wt_games_sold=wt_games_sold,
        wt_predictions=wt_predictions
    )
    logger.info('data weight update')
    return weights_qry.first()


def create_default_weights(
    *,
    player_id: Optional[int] = None
) -> Union[DataWeights, None]:
    """
    create a default weights to player or general
    """
    data = dict(
        wt_games=DEFAULT_WEIGHTS['WT_GAMES'],
        wt_sets=DEFAULT_WEIGHTS['WT_SETS'],
        wt_points=DEFAULT_WEIGHTS['WT_POINTS'],
        wt_games_sold=DEFAULT_WEIGHTS['WT_GAMES_SOLD'],
        wt_predictions=DEFAULT_WEIGHTS['WT_PREDICTIONS'],
        player_id=player_id
    )
    default_wt_qry = selectors. \
        filter_default_data_weights()
    if default_wt_qry.exists() and not player_id:
        if not player_id:
            return
        default_ = default_wt_qry.first()[0]
        default_.pop('player_id')
        default_.pop('id')
        data.update(**default_)
    return create_or_update_data_weights(**data)
