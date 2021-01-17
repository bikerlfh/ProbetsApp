from typing import Dict, Any, Optional
from datetime import datetime

import pandas as pd

from apps.games import selectors as games_selectors
from apps.games.constants import GameStatus
from apps.data.weights import wt_player


def get_games_predictions_by_wt_player(
    start_dt: str,
    min_diff: Optional[int] = 39
) -> Dict[str, Any]:
    start_dt = datetime.strptime(start_dt, '%Y-%m-%d')
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
        wt_score = wt_player.get_player_scores_by_game(
            h_id=h_id,
            a_id=a_id
        )
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
    l_pt = t_predictions - w_pt
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
