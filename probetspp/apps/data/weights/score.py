from typing import Union, Dict, Any, Optional, List
from decimal import Decimal
import pandas as pd

from apps.games import statistics, selectors as games_selectors
from apps.data.weights import selectors, services


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


def get_game_score_by_game_id(
    *,
    game_id: int
) -> Dict[str, Any]:
    game = games_selectors.\
        filter_game_by_id(game_id=game_id).first()
    h_wt_score = get_wt_score_player(player_id=game.h_id)
    a_wt_score = get_wt_score_player(player_id=game.a_id)
    data = dict(
        h_wt_score=h_wt_score,
        a_wt_score=a_wt_score
    )
    return data

from datetime import datetime, date
from apps.games.constants import GameStatus


def get_games_wt_score_by_player(
    *,
    start_at: Optional[date] = None,
    status: Optional[int] = None,
    min_diff: Optional[int] = None,
    min_total_games: Optional[int] = None
) -> List[Dict[str, Any]]:
    if not start_at:
        start_at = date.today()
    if not status:
        status = GameStatus.SCHEDULED.value
    if min_diff is None:
        min_diff = 50
    if min_total_games is None:
        min_total_games = 10

    games_qry = games_selectors.filter_games(
        start_dt=start_at,
        status=status,
        filter_=dict(
            home_player__stats__total_games__gte=min_total_games,
            away_player__stats__total_games__gte=min_total_games
        )
    )
    data_games = []
    for game in games_qry:
        h_id = game.h_id
        a_id = game.a_id

        wt_score = get_game_score_by_game_id(
            game_id=game.id
        )
        h_wt_score = wt_score['h_wt_score']
        a_wt_score = wt_score['a_wt_score']
        if h_wt_score < 0 and a_wt_score < 0:
            continue
        if h_wt_score > a_wt_score:
            diff = h_wt_score - a_wt_score
        else:
            diff = a_wt_score - h_wt_score
        if diff >= min_diff:
            data_games.append(dict(
                id=game.id,
                h_id=h_id,
                a_id=a_id,
                **wt_score
            ))
    return data_games


def get_games_predictions_by_wt_player(
    date: str,
    min_diff: Optional[int] = 39
) -> Dict[str, Any]:
    start_dt = datetime.strptime(date, '%Y-%m-%d')
    games_qry = games_selectors.filter_games(
        start_dt=start_dt,
        status=GameStatus.FINISHED.value,
        filter_=dict(
            home_player__stats__total_games__gte=10,
            away_player__stats__total_games__gte=10
        )
    )
    data_games = []
    p_w_score = 0
    p_l_score = 0
    for game in games_qry:
        winner_id = game.winner_id
        h_id = game.h_id
        a_id = game.a_id
        data_ = dict(
            id=game.id,
            h_id=h_id,
            a_id=h_id,
            winner_id=winner_id

        )
        wt_score = get_game_score_by_game_id(game_id=game.id)
        h_wt_score = wt_score['h_wt_score']
        a_wt_score = wt_score['a_wt_score']
        if h_wt_score < 0 and a_wt_score < 0:
            continue

        if h_wt_score > a_wt_score:
            diff = h_wt_score - a_wt_score
            ptd_won = winner_id == h_id

        else:
            diff = a_wt_score - h_wt_score
            ptd_won = winner_id == a_id
        if diff >= min_diff:
            p_w_score += diff if ptd_won else 0
            p_l_score += diff if not ptd_won else 0
            data_.update(
                ptd_won=ptd_won,
                **wt_score
            )
            data_games.append(data_)

    df = pd.DataFrame(data_games)
    t_predictions = len(data_games)
    w_pt = len(df[df['ptd_won']])
    l_pt = len(df[df['ptd_won'] == False])
    per_ = 100 * (w_pt / t_predictions)

    p_w_score = (p_w_score / t_predictions)
    p_l_score = (p_l_score / t_predictions)
    data = dict(
        min_diff=min_diff,
        t_predictions=len(data_games),
        w_pt=w_pt,
        l_pt=l_pt,
        w_per=per_,
        p_w_score=p_w_score,
        p_l_score=p_l_score
    )
    return data




