from decimal import Decimal
from typing import Dict, Any

from apps.games import statistics
from apps.data import services
from apps.data.weights import wt_core


def get_wt_score_player(
    *,
    player_id: int
) -> Decimal:
    """
    calculate wt score player
    Attrs:
        player_id: player identification
    Return: wt_score
    """
    wt_player = services.get_data_weights_player(
        player_id=player_id
    )
    stats = statistics. \
        get_player_stats_data(player_id=player_id)

    wt_g = wt_player['wt_games']
    wt_sets = wt_player['wt_sets']
    wt_points = wt_player['wt_points']
    wt_g_sold = wt_player['wt_games_sold']
    wt_predictions = wt_player['wt_predictions']
    t_g = stats['t_games']
    w_g = stats['w_games']
    l_g = stats['l_games']
    w_sts = stats['w_sets']
    l_sts = stats['l_sets']
    w_pts = stats['w_points']
    l_pts = stats['l_points']
    g_sold = stats['g_sold']
    t_pdt = stats['t_predictions']
    w_pdt = stats['w_predictions']
    l_pdt = stats['l_predictions']
    t_sts = w_sts + l_sts
    t_pts = w_pts + l_pts
    s_g = wt_core.calculate_score_item(wt_g, t_g, w_g, l_g)
    s_sts = wt_core.calculate_score_item(wt_sets, t_sts, w_sts, l_sts)
    s_pts = wt_core.calculate_score_item(wt_points, t_pts, w_pts, l_pts)
    s_g_sold = wt_core.calculate_score_item(wt_g_sold, t_g, g_sold, 0)
    s_pdt = wt_core.calculate_score_item(wt_predictions, t_pdt, w_pdt, l_pdt)
    score = s_g + s_sts + s_pts + s_pdt - s_g_sold
    return score


def get_player_scores_by_game(
    *,
    h_id: int,
    a_id: int
) -> Dict[str, Any]:
    """
    get weight score to h_player and a_player
    Attr:
        h_id: home player identifier
        a_id: away player identifier
    Return: dict(
        h_wt_score: home player weight score
        a_wt_score: away player weight score
    )
    """
    h_wt_score = get_wt_score_player(player_id=h_id)
    a_wt_score = get_wt_score_player(player_id=a_id)
    data = dict(
        h_wt_score=h_wt_score,
        a_wt_score=a_wt_score
    )
    return data
