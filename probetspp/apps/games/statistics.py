import logging
from typing import Dict, Any, Union, List, Optional

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
    h_b2w = False
    a_b2w = False
    h_points = 0
    a_points = 0
    num_set = 0
    h_sets = 0
    a_sets = 0
    line_score = game_data['l_score']
    h_id = game_data['h_id']
    h_is_winner = game_data['winner_id'] == h_id
    for set_score in line_score:
        num_set += 1
        h_set_point = set_score['home']
        a_set_point = set_score['away']
        h_points += h_set_point
        a_points += a_set_point
        if h_set_point > a_set_point:
            h_sets += 1
        else:
            a_sets += 1
        if num_set == 2 or num_set == 3:
            if a_sets >= 2:
                h_b2w = h_is_winner
            elif h_sets >= 2:
                a_b2w = not h_is_winner

    game_data.update(
        num_set=num_set,
        h_points=h_points,
        h_b2w=h_b2w,
        a_points=a_points,
        a_b2w=a_b2w,
    )
    return game_data


def get_game_stats(
    *,
    game_id: Optional[int] = None,
    games_id: Optional[List[int]] = None
) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
    """
    get game stats only status game FINISHED
    Attrs:
        game_id: game id
        games_id: list of games id
    Returns:
        List: dicts of games stats data if games_id is specified
        Dict: game data (
            id: game id
            status: game status
            league_id: game league id
            start_dt: game start_dt
            h_id: home player id
            a_id: away player id
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
    assert game_id or games_id, (
        'game_id or games_id are required'
    )
    stats_qry = games_selectors.filter_game_stats_data(
        game_id=game_id or games_id,
        status=GameStatus.FINISHED.value
    )
    stats = []
    for item in stats_qry:
        game_data = _add_line_score_data(game_data=item)
        stats.append(game_data)
    if isinstance(game_id, int):
        return stats[0] if stats else None
    return stats


def get_player_stats_data(
    *,
    player_id: Optional[int] = None,
    players_id: Optional[List[int]] = None
) -> Union[List[Dict[str, Any]], Dict[str, Any], None]:
    assert player_id or players_id, (
        'player_id or players_id are required'
    )
    stats_qry = games_selectors.filter_player_stats_data(
        player_id=player_id or players_id
    )
    if player_id:
        return stats_qry.first()
    return list(stats_qry)


def recalculate_player_stats(
    *,
    player_id: int
) -> Union[None]:
    """
    Recalculate player stats
    """
    games_id = games_selectors.filter_games_by_player_id(
        player_id=player_id
    ).values_list('id', flat=True)
    games_stats = get_game_stats(
        games_id=list(games_id)
    )
    player_stats = games_selectors.\
        get_player_stats_by_player_id(player_id=player_id)
    t_games = 0
    w_games = 0
    l_games = 0
    w_score = 0
    l_score = 0
    w_points = 0
    l_points = 0
    b2w = 0
    b2l = 0
    for game_ in games_stats:
        t_games += 1
        a_id = game_['a_id']
        p_ = 'h'
        vs_ = 'a'
        if a_id == player_id:
            p_ = 'a'
            vs_ = 'h'
        winner_id = game_['winner_id']
        w_score += game_[f'{p_}_score']
        l_score += game_[f'{vs_}_score']
        w_points += game_[f'{p_}_points']
        l_points += game_[f'{vs_}_points']
        b2w += 1 if game_[f'{p_}_b2w'] else 0
        b2l += 1 if game_[f'{vs_}_b2w'] else 0
        if winner_id == player_id:
            w_games += 1
            continue
        l_games += 1
    player_stats.total_games = t_games
    player_stats.won_games = w_games
    player_stats.lost_games = l_games
    player_stats.won_sets = w_score
    player_stats.lost_sets = l_score
    player_stats.won_points = w_points
    player_stats.lost_points = l_points
    player_stats.back_to_win = b2w
    player_stats.back_to_lose = b2l
    player_stats.save()
    logger.info(
        f'recalculate_player_stats :: player '
        f'{player_id} stats has been recalculated'
    )
