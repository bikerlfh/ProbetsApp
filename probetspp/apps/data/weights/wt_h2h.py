from typing import Dict, Any
from decimal import Decimal
from apps.data.weights import wt_games
from apps.data import services


def get_h2h_wt_score(
    *,
    h_id: int,
    a_id: int,
    h2h_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    get h2h wt score
    Attrs:
        h_id: home player id
        a_id: away player id
        h2h_data: h2h data
    Return: dict(
        t_h2h: total games
        h_h2h_wt_score: home player h2h wt_score
        h_h2h_wt_score: away player h2h wt_score
    )
    """
    home_wins = h2h_data['home_wins']
    away_wins = h2h_data['away_wins']
    t_h2h = home_wins + away_wins
    data = dict(
        t_h2h=t_h2h,
        h_h2h_wt_score=0,
        a_h2h_wt_score=0
    )
    if t_h2h == 0:
        return data
    h_wt = services.get_data_weights_player(
        player_id=h_id
    )['wt_h2h']
    a_wt = services.get_data_weights_player(
        player_id=a_id
    )['wt_h2h']
    h_wt_score = 0
    a_wt_score = 0
    for game in h2h_data['games']:
        score = wt_games.get_game_wt_score(
            game_data=game
        )
        if game['h_id'] == h_id:
            h_wt_score += score['h_game_wt_score']
            continue
        a_wt_score += score['a_game_wt_score']
    h_h2h_wt_score = h_wt * Decimal(h_wt_score / t_h2h)
    a_h2h_wt_score = a_wt * Decimal(a_wt_score / t_h2h)
    """h_h2h_wt_score = wt_core.calculate_score_item(
        h_wt, t_h2h, home_wins, away_wins
    )
    a_h2h_wt_score = wt_core.calculate_score_item(
        a_wt, t_h2h, away_wins, home_wins
    )"""
    data.update(
        h_h2h_wt_score=h_h2h_wt_score,
        a_h2h_wt_score=a_h2h_wt_score
    )
    return data
