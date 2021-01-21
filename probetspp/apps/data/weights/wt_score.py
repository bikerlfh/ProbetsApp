from datetime import date, datetime
from typing import Dict, Any, Optional, List
from apps.games import services as games_services
from apps.data.weights import wt_player, wt_games, wt_h2h


def _get_last_game_wt_score(
    *,
    game: Dict[str, Any]
) -> Dict[str, Any]:
    h_lg_wt_score = wt_games.get_last_games_player_wt_score(
        player_id=game['home_player']['id'],
        games_data=game['h_last_games']
    )
    a_lg_wt_score = wt_games.get_last_games_player_wt_score(
        player_id=game['away_player']['id'],
        games_data=game['a_last_games']
    )
    return dict(
        h_lg_wt_score=h_lg_wt_score,
        a_lg_wt_score=a_lg_wt_score
    )


def get_games_score_data_to_predict(
    *,
    game_id: Optional[int] = None,
    start_dt: Optional[date] = None,
    start_dt_range: Optional[List[datetime]] = None,
    status: Optional[int] = None,
    h2h_games_limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    get games score data to predict
    Attrs:
        game_id: game id
        start_dt: game start date
        start_dt_range: list of datetime [
            from_date,
            to_date
        ]
        status: game status
        h2h_games_limit: h2h games limit
    Return: list to dict
    """
    filter_ = None
    if start_dt_range:
        filter_ = dict(
            start_dt__gte=start_dt_range[0],
            start_dt__lte=start_dt_range[1]
        )
    game_data = games_services.get_games_data_to_predict(
        game_id=game_id,
        start_dt=start_dt,
        status=status,
        filter_=filter_,
        h2h_games_limit=h2h_games_limit
    )
    game_score_data = []
    for game in game_data:
        h_id = game['home_player']['id']
        a_id = game['away_player']['id']
        p_wt_score = wt_player.get_player_scores_by_game(
            h_id=h_id,
            a_id=a_id
        )
        h2h_wt_score = wt_h2h.get_h2h_wt_score(
            h_id=h_id,
            a_id=a_id,
            h2h_data=game['h2h_games_data']
        )
        last_games_wt_score = _get_last_game_wt_score(game=game)

        d_g_wt_score = wt_games.get_direct_opponents_wt_score(
            h_id=h_id,
            a_id=a_id,
            h_last_games=game['h_last_games'],
            a_last_games=game['a_last_games'],
        )
        data = dict(
            game_id=game['id'],
            h_id=h_id,
            a_id=a_id,
            **p_wt_score,
            **h2h_wt_score,
            **last_games_wt_score,
            **d_g_wt_score
        )
        game_score_data.append(data)
    return game_score_data
