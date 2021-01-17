from datetime import date
from typing import Dict, Any, Optional, List

import pandas as pd

from apps.games.constants import GameStatus
from apps.games import selectors as games_selectors
from apps.data.constants import (
    MIN_DIFF_PLAYER_SCORE,
    MIN_TOTAL_GAMES_PLAYER
)
from apps.data import services
from apps.data.weights import wt_player


def get_games_prediction_by_wt_score_player(
    *,
    start_dt: Optional[date] = None,
    status: Optional[int] = None,
    min_diff: Optional[int] = None,
    min_total_games: Optional[int] = None,
    create_data_game: Optional[bool] = False
) -> List[Dict[str, Any]]:
    """
    get games prediction by wt_score_player
    Attrs:
        start_dt: game start_dt
        status: status of game
        min_diff: diff between players
                  score to predicted
        min_total_games: min of number of total games
                         to player to can predicted
    Return: dict(
        id: game id
        h_id: home player id
        a_id: away player id
        winner_id: winner id of game (only its finished)
        winner_id_pdt: player_id winner of prediction,
        h_wt_score: home player wt score
        a_wt_score: away player wt score,
        diff: diff between h_wt_score and a_wt_score
    )
    """
    if not start_dt:
        start_dt = date.today()
    if not status:
        status = GameStatus.SCHEDULED.value
    if min_diff is None:
        min_diff = MIN_DIFF_PLAYER_SCORE
    if min_total_games is None:
        min_total_games = MIN_TOTAL_GAMES_PLAYER

    games_qry = games_selectors.filter_games(
        start_dt=start_dt,
        status=status,
        filter_=dict(
            home_player__stats__total_games__gte=min_total_games,
            away_player__stats__total_games__gte=min_total_games
        )
    )
    data_games = []
    for game in games_qry:
        game_id = game.id
        h_id = game.h_id
        a_id = game.a_id
        wt_score = wt_player.get_player_scores_by_game(
            h_id=h_id,
            a_id=a_id
        )
        h_wt_score = wt_score['h_wt_score']
        a_wt_score = wt_score['a_wt_score']
        winner_id_pdt = h_id
        if h_wt_score < 0 and a_wt_score < 0:
            continue
        if h_wt_score > a_wt_score:
            diff = h_wt_score - a_wt_score
        else:
            diff = a_wt_score - h_wt_score
            winner_id_pdt = a_id
        if diff >= min_diff:
            data_games.append(dict(
                id=game_id,
                h_id=h_id,
                a_id=a_id,
                # only if game is finished
                winner_id=game.winner_id,
                winner_id_pdt=winner_id_pdt,
                diff=diff,
                **wt_score
            ))
            if not create_data_game:
                continue
            services.create_or_update_data_game(
                game_id=game_id,
                min_wt_p_diff=min_diff,
                h_wt_score=h_wt_score,
                a_wt_score=a_wt_score
            )
    return data_games


def get_games_finished_predictions_by_score_player(
    *,
    start_dt: date,
    min_diff: Optional[int] = None
) -> Dict[str, Any]:
    """
    get prediction of games finished by score players
    Attrs:
        start_dt: game start date
        min_diff: min diff between wt player scores
    Return: dict(
        min_diff: min diff
        t_predictions: total productions
        w_pdt: num predictions won
        l_pdt: num predictions lose
        w_per: won predictions percentage
        p_w_score: average score for won games
        p_l_score: average score for lost games
    )
    """
    games_qry = get_games_prediction_by_wt_score_player(
        status=GameStatus.FINISHED.value,
        start_dt=start_dt,
        min_diff=min_diff
    )
    data_games = []
    w_score = 0
    l_score = 0
    for g_data in games_qry:
        winner_id = g_data['winner_id']
        winner_id_pdt = g_data['winner_id_pdt']
        diff = g_data['diff']
        pdt_won = winner_id == winner_id_pdt
        w_score += diff if pdt_won else 0
        l_score += diff if not pdt_won else 0
        data_ = dict(
            **g_data,
            pdt_won=pdt_won
        )
        data_games.append(data_)

    df = pd.DataFrame(data_games)
    t_predictions = len(data_games)
    if t_predictions == 0:
        return dict(
            min_diff=min_diff,
            t_predictions=t_predictions
        )
    w_pdt = len(df[df['pdt_won']])
    l_pdt = t_predictions - w_pdt
    per_ = 100 * (w_pdt / t_predictions)
    avr_w_score = (w_score / t_predictions)
    avr_l_score = (l_score / t_predictions)
    data = dict(
        min_diff=min_diff,
        t_predictions=t_predictions,
        w_pdt=w_pdt,
        l_pdt=l_pdt,
        w_per=per_,
        avr_w_score=avr_w_score,
        avr_l_score=avr_l_score
    )
    return data
