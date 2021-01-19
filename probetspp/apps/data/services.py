import logging
from decimal import Decimal
from typing import Optional, Union, Dict, Any

from apps.games import selectors as games_selectors
from apps.data.models import DataWeights, DataGame
from apps.data.constants import DEFAULT_WEIGHTS
from apps.data import selectors

logger = logging.getLogger(__name__)


def create_weights(
    *,
    wt_games: Decimal,
    wt_sets: Decimal,
    wt_points: Decimal,
    wt_games_sold: Decimal,
    wt_predictions: Decimal,
    wt_h2h: Decimal,
    wt_last_games: Decimal,
    wt_direct_opponents: Decimal,
    player_id: Optional[int] = None,
) -> DataWeights:
    weight = DataWeights.objects.create(
        player_id=player_id,
        wt_games=wt_games,
        wt_sets=wt_sets,
        wt_points=wt_points,
        wt_games_sold=wt_games_sold,
        wt_predictions=wt_predictions,
        wt_h2h=wt_h2h,
        wt_last_games=wt_last_games,
        wt_direct_opponents=wt_direct_opponents
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
    wt_h2h: Decimal,
    wt_last_games: Decimal,
    wt_direct_opponents: Decimal,
    player_id: Optional[int] = None
) -> Union[DataWeights, None]:
    data = dict(
        wt_games=wt_games,
        wt_sets=wt_sets,
        wt_points=wt_points,
        wt_games_sold=wt_games_sold,
        wt_predictions=wt_predictions,
        wt_h2h=wt_h2h,
        wt_last_games=wt_last_games,
        wt_direct_opponents=wt_direct_opponents,
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
    weights_qry.update(**data)
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
        **DEFAULT_WEIGHTS,
        player_id=player_id
    )
    default_wt_qry = selectors. \
        filter_default_data_weights()
    if default_wt_qry.exists() and not player_id:
        default_ = default_wt_qry.first()
        default_.pop('player_id')
        default_.pop('id')
        data.update(**default_)
    return create_or_update_data_weights(**data)


def create_or_update_data_game(
    *,
    game_id: int,
    min_wt_p_diff: Decimal,
    h_wt_score: Decimal,
    a_wt_score: Decimal,
    min_h2h_wt_diff: Decimal,
    h_h2h_wt_score: Decimal,
    a_h2h_wt_score: Decimal,
    min_l_g_wt_diff: Decimal,
    h_l_g_wt_score: Decimal,
    a_l_g_wt_score: Decimal,
    min_d_opp_wt_diff: Decimal,
    h_d_opp_wt_score: Decimal,
    a_d_opp_wt_score: Decimal
) -> Union[None]:
    data_game_qry = selectors.filter_data_game_by_game_id(
        game_id=game_id
    )
    data = dict(
        game_id=game_id,
        min_wt_p_diff=min_wt_p_diff,
        h_wt_score=h_wt_score,
        a_wt_score=a_wt_score,
        min_h2h_wt_diff=min_h2h_wt_diff,
        h_h2h_wt_score=h_h2h_wt_score,
        a_h2h_wt_score=a_h2h_wt_score,
        min_l_g_wt_diff=min_l_g_wt_diff,
        h_l_g_wt_score=h_l_g_wt_score,
        a_l_g_wt_score=a_l_g_wt_score,
        min_d_opp_wt_diff=min_d_opp_wt_diff,
        h_d_opp_wt_score=h_d_opp_wt_score,
        a_d_opp_wt_score=a_d_opp_wt_score
    )
    if data_game_qry.exists():
        data_game_qry.update(**data)
        return
    DataGame.objects.create(**data)


def get_data_weights_player(
    *,
    player_id: int
) -> Dict[str, Any]:
    p_wt_qry = selectors.filter_data_weights_by_player_id(
        player_id=player_id
    )
    if p_wt_qry.exists():
        return p_wt_qry.first()
    d_wt_qry = selectors.filter_default_data_weights()
    return d_wt_qry.first()
