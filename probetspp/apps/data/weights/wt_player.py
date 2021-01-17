from decimal import Decimal
from typing import Dict, Any

from apps.games import statistics
from apps.data import selectors


def _calculate_score_item(
    wt: Decimal,
    total: int,
    won: int,
    lost: int
) -> Decimal:
    if total == 0:
        return Decimal(0)
    w_per = 100 * (won / total)
    l_per = 100 * (lost / total)
    score = wt * Decimal(w_per - l_per)
    return Decimal(score)


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
    data_wt_qry = selectors.filter_data_weights_by_player_id(
        player_id=player_id
    )
    if not data_wt_qry.exists():
        data_wt_qry = selectors.filter_default_data_weights()

    wt_player = data_wt_qry.first()

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
    s_g = _calculate_score_item(wt_g, t_g, w_g, l_g)
    s_sts = _calculate_score_item(wt_sets, t_sts, w_sts, l_sts)
    s_pts = _calculate_score_item(wt_points, t_pts, w_pts, l_pts)
    s_g_sold = _calculate_score_item(wt_g_sold, t_g, g_sold, 0)
    s_pdt = _calculate_score_item(wt_predictions, t_pdt, w_pdt, l_pdt)
    score = s_g + s_sts + s_pts + s_g_sold + s_pdt
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
