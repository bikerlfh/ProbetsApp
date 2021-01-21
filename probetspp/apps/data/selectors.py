from typing import Optional
from django.db.models import QuerySet

from apps.data.models import DataWeights, DataGame, AcceptanceValue


def filter_default_data_weights() -> 'QuerySet[DataWeights]':
    return DataWeights.objects.filter(
        player_id__isnull=True
    ).values(
        'id',
        'wt_games',
        'wt_sets',
        'wt_points',
        'wt_games_sold',
        'wt_predictions',
        'player_id',
        'wt_h2h',
        'wt_last_games',
        'wt_direct_opponents'
    )


def filter_data_weights_by_player_id(
    *,
    player_id: int
) -> 'QuerySet[DataWeights]':
    return DataWeights.objects.filter(
        player_id=player_id
    ).values(
        'id',
        'wt_games',
        'wt_sets',
        'wt_points',
        'wt_games_sold',
        'wt_predictions',
        'player_id',
        'wt_h2h',
        'wt_last_games',
        'wt_direct_opponents'
    )


def filter_data_game_by_game_id(
    *,
    game_id: int
) -> 'QuerySet[DataGame]':
    return DataGame.objects.filter(
        game_id=game_id
    ).values(
        'id',
        'game_id',
        'acceptance_value_id',
        'h_wt_score',
        'a_wt_score',
        'h_h2h_wt_score',
        'a_h2h_wt_score',
        'h_l_g_wt_score',
        'a_l_g_wt_score',
        'h_d_opp_wt_score',
        'a_d_opp_wt_score',
    )


def filter_acceptance_value_active() -> 'QuerySet[AcceptanceValue]':
    return AcceptanceValue.objects.filter(
        is_active=True
    ).values(
        'id',
        'p_wt_diff',
        'h2h_wt_diff',
        'l_g_wt_diff',
        'd_opp_wt_diff',
        'is_active'
    )
