from django.db.models import QuerySet

from apps.data.models import DataWeights, DataGame


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
        'player_id'
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
        'player_id'
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
        'h_wt_score',
        'a_wt_score'
    )
