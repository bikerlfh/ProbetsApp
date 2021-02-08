import logging
from datetime import date
from typing import Dict, Any, Union, List, Optional

import pandas as pd
import numpy as np

from apps.games.constants import GameStatus
from apps.games import selectors as games_selectors


logger = logging.getLogger(__name__)


def _add_line_score_data(
    *,
    game_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    add line score data to game_data
    Attrs:
        game_data: game stats data
    Returns: game_data.update(
        num_set: number of sets
        h_points: home points
        h_b2w: home back to win
        a_points: away points
        a_b2w: away back to win
    )
    """
    h_id = game_data['h_id']
    a_id = game_data['a_id']
    winner_id = game_data['winner_id']
    if not game_data['l_score']:
        return game_data
    df = pd.DataFrame(game_data['l_score'])
    sum_pts = df.sum()
    h_points = sum_pts['home']
    a_points = sum_pts['away']
    df['win'] = np.where(df['home'] > df['away'], 1, 2)
    h_no_in = 1 not in df[:2]['win'] or 1 not in df[1:3]['win']
    a_no_in = 2 not in df[:2]['win'] or 2 not in df[1:3]['win']
    h_b2w = h_no_in and winner_id == h_id
    a_b2w = a_no_in and winner_id == a_id
    game_data.update(
        num_set=len(df),
        h_points=h_points,
        h_b2w=h_b2w,
        a_points=a_points,
        a_b2w=a_b2w
    )
    return game_data


def get_games_stats(
    *,
    game_id: Optional[Union[List[int], int]] = None,
    player_id: Optional[int] = None,
    league_id: Optional[int] = None,
    status: Optional[int] = None,
    start_dt: Optional[date] = None,
    h2h_players_id: Optional[List[int]] = None,
    limit: Optional[int] = None,
    filter_: Optional[Dict[str, Any]] = None
) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
    """
    get game stats only status game FINISHED
    Attrs:
        game_id: game id or list of game_id
        league_id: league identifier
        status: game status
        start_dt: date of game
        h2h_players_id: list of 2 h2h players id
        limit: limit of rows
    Returns:
        List: dicts of games stats data if games_id is specified
        Dict: game data (
            id: game id
            status: game status
            league_id: game league id
            start_dt: game start_dt
            h_id: home player id
            a_id: away player id
            h_name: home player name
            a_name: away player name
            h_score: home score
            a_score: away score
            l_score: line score
            winner_id: winner player id
            num_set: number of sets
            h_points: home points
            h_b2w: home back to win
            a_points: away points
            a_b2w: away back to win
        )
    """
    stats_qry = games_selectors.filter_game_stats_data(
        game_id=game_id,
        player_id=player_id,
        league_id=league_id,
        status=status,
        start_dt=start_dt,
        h2h_players_id=h2h_players_id,
        filter_=filter_
    )
    if limit:
        stats_qry = stats_qry[:limit]
    stats = []
    for item in stats_qry:
        game_data = _add_line_score_data(game_data=item)
        stats.append(game_data)
    if isinstance(game_id, int):
        return stats[0] if stats else None
    return stats


def get_last_player_games_data(
    *,
    player_id: int,
    from_dt: Optional[date] = None,
    to_dt: Optional[date] = None,
    limit: Optional[int] = None
) -> List[Dict[str, Any]]:
    """
    get last player games (stats data)
    Attrs:
        player_id: player identification
        from_dt: from date of games
        to_dt: to date of games
        limit: limit of games
    """
    if not to_dt:
        to_dt = date.today()
    filter_ = dict(
        start_dt__date__lte=to_dt
    )
    if from_dt:
        filter_.update(
            start_dt__date__gte=from_dt
        )
    return get_games_stats(
        player_id=player_id,
        status=GameStatus.FINISHED.value,
        filter_=filter_,
        limit=limit
    )


def get_player_stats_data(
    *,
    player_id: Union[List[int], int]
) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
    """
    Return dict or list of dict(
        id: PlayerStats_id,
        player_id: player identifier
        t_games: total games
        w_games: won games
        l_games: lost games
        w_sets: won sets
        l_sets: lost sets
        w_points: won points
        l_points: lost points
        b2w: back to win
        b2l: back to lose
        g_sold: games sold
        t_predictions: win predictions
        w_predictions: win predictions
        l_predictions: lost predictions
        cp: confidence %
    )
    """
    stats_qry = games_selectors.filter_player_stats_data(
        player_id=player_id
    )
    if isinstance(player_id, int):
        return stats_qry.first()
    return list(stats_qry)


def recalculate_player_stats(
    *,
    player_id: int
) -> Union[None]:
    """
    Recalculate player stats
    """
    games_stats = get_games_stats(
        player_id=player_id,
        status=GameStatus.FINISHED.value
    )
    player_stats = games_selectors.\
        get_player_stats_by_player_id(player_id=player_id)

    df = pd.DataFrame(games_stats)
    t_games = len(df)
    w_games = len(df[(df['winner_id'] == player_id)])
    df['p_b2w'] = np.where(df['h_id'] == player_id, df['h_b2w'], df['a_b2w'])
    df['p_b2l'] = np.where(df['h_id'] != player_id, df['h_b2w'], df['a_b2w'])

    player_stats.total_games = t_games
    player_stats.won_games = w_games
    player_stats.lost_games = t_games - w_games
    player_stats.won_sets = np.where(
        df['h_id'] == player_id, df['h_score'], df['a_score']
    ).sum()
    player_stats.lost_sets = np.where(
        df['h_id'] != player_id, df['h_score'], df['a_score']
    ).sum()
    player_stats.won_points = np.where(
        df['h_id'] == player_id, df['h_points'], df['a_points']
    ).sum()
    player_stats.lost_points = np.where(
        df['h_id'] != player_id, df['h_points'], df['a_points']
    ).sum()
    player_stats.back_to_win = len(df[(df['p_b2w'])])
    player_stats.back_to_lose = len(df[(df['p_b2l'])])
    player_stats.save()
    logger.info(
        f'recalculate_player_stats :: player '
        f'{player_id} stats has been recalculated'
    )
