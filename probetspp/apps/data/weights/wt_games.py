from typing import Dict, Any, List
from decimal import Decimal

import pandas as pd
import numpy as np

from apps.data import services
from apps.data.weights import wt_core


def get_game_wt_score(
    *,
    game_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    get game wt score (player)
    Attrs:
        game_data:  game data
    Return: dict(
        h_game_wt_score: home player wt_score for game
        a_game_wt_score: away player wt_score for game
    )
    """
    h_id = game_data['h_id']
    a_id = game_data['a_id']
    h_score = game_data['h_score']
    h_points = game_data.get('h_points', 0)
    a_score = game_data['a_score']
    a_points = game_data.get('a_points', 0)

    h_wt = services.get_data_weights_player(
        player_id=h_id
    )
    a_wt = services.get_data_weights_player(
        player_id=a_id
    )
    h_wt_sets = h_wt['wt_sets']
    h_wt_points = h_wt['wt_points']
    a_wt_sets = a_wt['wt_sets']
    a_wt_points = a_wt['wt_points']

    t_points = a_points + h_points

    h_wt_st_score = (h_score * 10) * h_wt_sets
    a_wt_st_score = (a_score * 10) * a_wt_sets
    h_wt_pts_score = 0
    a_wt_pts_score = 0
    if t_points > 0:
        h_wt_pts_score = wt_core.calculate_score_item(
            h_wt_points, t_points, h_points, a_points
        )
        a_wt_pts_score = wt_core.calculate_score_item(
            a_wt_points, t_points, a_points, h_points
        )
    h_game_wt_score = h_wt_st_score + h_wt_pts_score
    a_game_wt_score = a_wt_st_score + a_wt_pts_score
    data = dict(
        h_game_wt_score=h_game_wt_score,
        a_game_wt_score=a_game_wt_score
    )
    return data


def get_last_games_player_wt_score(
    *,
    player_id: int,
    games_data: List[Dict[str, Any]]
) -> Decimal:
    player_wt = services.get_data_weights_player(
        player_id=player_id
    )
    wt_score = 0
    wt_last_games = player_wt['wt_last_games']
    t_games = 0
    if len(games_data) == 0:
        return Decimal(0)
    for game in games_data:
        h_id = game['h_id']
        a_id = game['a_id']
        if player_id != h_id and player_id != a_id:
            continue
        t_games += 1
        score_data = get_game_wt_score(game_data=game)
        if h_id == player_id:
            wt_score += score_data['h_game_wt_score']
            continue
        wt_score += score_data['a_game_wt_score']

    player_wt_score = wt_last_games * (wt_score / t_games)
    return player_wt_score


def __calculate_direct_opponents_wt_score(
    *,
    h_id: int,
    a_id: int,
    h_d_opp_games: List[Dict[str, Any]],
    a_d_opp_games: List[Dict[str, Any]]
) -> Dict[str, Any]:
    """
    Return: dict(
        h_d_opp_wt_score: home player direct opponents wt_score
        h_d_opp_wt_score: away player direct opponents wt_score
    )
    """
    a_df = pd.DataFrame(a_d_opp_games)
    h_d_opp_wt_score = 0
    a_d_opp_wt_score = 0
    t_games = 0
    data = dict(
        h_d_opp_wt_score=h_d_opp_wt_score,
        a_d_opp_wt_score=a_d_opp_wt_score
    )
    if not h_d_opp_games or not a_d_opp_games:
        return data
    for game in h_d_opp_games:
        vs_id = game['vs_id']
        a_game = a_df[a_df['vs_id'] == vs_id]
        if len(a_df) == 0:
            break
        if len(a_game) == 0:
            continue
        h_g_h_id = game['h_id']
        h_wt_score = get_game_wt_score(game_data=game)
        a_game = a_game.to_dict(orient='records')[0]
        a_g_h_id = a_game['h_id']
        a_wt_score = get_game_wt_score(
            game_data=a_game
        )
        if h_id == h_g_h_id:
            h_d_opp_wt_score += h_wt_score['h_game_wt_score']
        else:
            h_d_opp_wt_score += h_wt_score['a_game_wt_score']

        if a_id == a_g_h_id:
            a_d_opp_wt_score += a_wt_score['h_game_wt_score']
        else:
            a_d_opp_wt_score += a_wt_score['a_game_wt_score']
        a_df = a_df[a_df['id'] != a_game['id']]
        t_games += 1
    a_d_opp_wt_score = (a_d_opp_wt_score / t_games)
    h_d_opp_wt_score = (h_d_opp_wt_score / t_games)
    data.update(
        h_d_opp_wt_score=h_d_opp_wt_score,
        a_d_opp_wt_score=a_d_opp_wt_score
    )
    return data


def get_direct_opponents_wt_score(
    h_id: int,
    a_id: int,
    h_last_games: List[Dict[str, Any]],
    a_last_games: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    get direct opponents wt score
    Attrs:
        h_id: home player id
        a_id: away player id
        h_last_games: home last games
        a_last_games: away last games
    """
    data = dict(
        h_d_opp_wt_score=0,
        a_d_opp_wt_score=0
    )
    h_df = pd.DataFrame(h_last_games)
    a_df = pd.DataFrame(a_last_games)
    if not h_last_games or not a_last_games:
        return data
    # exclude h2h
    h_df = h_df[(h_df['h_id'] != a_id) & (h_df['a_id'] != a_id)]
    a_df = a_df[(a_df['h_id'] != h_id) & (a_df['a_id'] != h_id)]

    if len(h_df) == 0 or len(a_df) == 0:
        return data
    h_df['vs_id'] = np.where(
        h_df['h_id'] != h_id, h_df['h_id'], h_df['a_id']
    )
    a_df['vs_id'] = np.where(
        a_df['h_id'] != a_id, a_df['h_id'], a_df['a_id']
    )
    # games of direct opponents
    h_d_opp_df = h_df[h_df['vs_id'].isin(a_df['vs_id'])]
    a_d_opp_df = a_df[a_df['vs_id'].isin(h_df['vs_id'])]
    data = __calculate_direct_opponents_wt_score(
        h_id=h_id,
        a_id=a_id,
        h_d_opp_games=h_d_opp_df.to_dict(orient='records'),
        a_d_opp_games=a_d_opp_df.to_dict(orient='records')
    )
    return data
