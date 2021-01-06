from typing import Dict, Any, Union

from apps.games.constants import GameStatus
from apps.games.models import Game, Player

from apps.games import selectors as games_selectors


def get_game_stats(
    *,
    game: Game
) -> Union[Dict[str, Any], None]:
    status = GameStatus(game.status)
    if status != GameStatus.FINISHED:
        return None
    h_id = game.home_player.id
    a_id = game.away_player.id
    line_score = game.line_score
    h_back_to_win = False
    a_back_to_win = False
    h_points = 0
    a_points = 0
    num_set = 0
    h_sets_won = 0
    a_sets_won = 0
    h_is_winner = game.is_winner(player_id=h_id)
    for set_score in line_score:
        num_set += 1
        h_set_point = set_score['home']
        a_set_point = set_score['away']
        h_points += h_set_point
        a_points += a_set_point
        if h_set_point > a_set_point:
            h_sets_won += 1
        else:
            a_sets_won += 1
        if num_set == 2 or num_set == 3:
            if a_sets_won >= 2:
                h_back_to_win = h_is_winner
            elif h_sets_won >= 2:
                a_back_to_win = not h_is_winner

    data = dict(
        num_sets=num_set,
        h_id=h_id,
        h_points=h_points,
        h_score=h_sets_won,
        h_back_to_win=h_back_to_win,
        h_winner=h_is_winner,
        a_id=a_id,
        a_points=a_points,
        a_score=a_sets_won,
        a_back_to_win=a_back_to_win,
        a_winner=not h_is_winner
    )
    return data


def get_player_stats_data(
    *,
    player: Player
) -> Dict[str, Any]:
    player_id = player.id
    stats = games_selectors.\
        get_player_stats(player_id=player_id)
    data = dict(
        id=player_id,
        name=player.name,
        total_games=stats.total_games,
        won_games=stats.won_games,
        lost_games=stats.lost_games,
    )
    return data
