import logging
from datetime import datetime, date
from typing import Union, Optional, Dict, Any, List

from apps.predictions import services as predictions_services

from apps.games.constants import GameStatus
from apps.games.models import (
    Game,
    League,
    Player,
    PlayerStats
)
from apps.games import selectors, statistics


logger = logging.getLogger(__name__)


def create_league(
    *,
    external_id: str,
    name: str,
    gender: int
) -> Union[League, None]:
    league_qry = selectors.filter_league_by_external_id(
        external_id=external_id,
        gender=gender
    )
    if league_qry.exists():
        logger.warning(
            f'league {external_id} already exists'
        )
        return league_qry.first()

    return League.objects.create(
        external_id=external_id,
        name=name,
        gender=gender
    )


def create_player(
    *,
    external_id: str,
    short_name: Optional[str] = None,
    name: str,
    gender: int
) -> Union[Player, None]:
    player_qry = selectors.filter_league_by_external_id(
        external_id=external_id
    )
    if player_qry.exists():
        logger.warning(
            f'player {external_id} already exists'
        )
        return player_qry.first()
    player = Player.objects.create(
        external_id=external_id,
        short_name=short_name,
        name=name,
        gender=gender
    )
    PlayerStats.objects.create(
        player=player
    )
    logger.info(
        f'create_player :: player '
        f'{external_id} has been created'
    )
    return player


def update_player_stats_by_game(
    *,
    game: Game
) -> Union[None]:
    """
    Update player stats when a game has been finished
    Attrs:
        game: game objects
    Returns: None
    """
    status = GameStatus(game.status)
    if status != GameStatus.FINISHED:
        return
    game_stats = statistics.get_games_stats(game_id=game.id)
    h_id = game_stats['h_id']
    a_id = game_stats['a_id']
    is_home_winner = game_stats['winner_id'] == h_id
    home_stats = selectors.get_player_stats_by_player_id(
        player_id=h_id
    )
    away_stats = selectors.get_player_stats_by_player_id(
        player_id=a_id
    )
    home_stats.total_games += 1
    away_stats.total_games += 1
    if is_home_winner:
        home_stats.won_games += 1
        away_stats.lost_games += 1
    else:
        away_stats.won_games += 1
        home_stats.lost_games += 1
    if game.line_score:
        h_score = game_stats['h_score']
        h_points = game_stats['h_points']
        a_score = game_stats['a_score']
        a_points = game_stats['a_points']

        home_stats.won_sets += h_score
        home_stats.lost_sets += a_score
        home_stats.won_points += h_points
        home_stats.lost_points += a_points

        away_stats.won_sets += a_score
        away_stats.lost_sets += h_score
        away_stats.won_points += a_points
        away_stats.lost_points += h_points

        h_back_to_win = game_stats['h_b2w']
        a_back_to_win = game_stats['a_b2w']
        if h_back_to_win:
            home_stats.back_to_win += 1
            away_stats.back_to_lose += 1
        elif a_back_to_win:
            away_stats.back_to_win += 1
            home_stats.back_to_lose += 1
    home_stats.save()
    away_stats.save()


def create_game(
    *,
    external_id: str,
    home_player_id: int,
    away_player_id: int,
    league_id: int,
    start_dt: datetime,
    home_score: Optional[int] = 0,
    away_score: Optional[int] = 0,
    line_score: Optional[Dict[str, Any]] = None,
    status: Optional[int] = None
) -> Union[None]:
    home_player = selectors.filter_player_by_id(
        player_id=home_player_id
    )
    if not home_player.exists():
        raise Exception(
            f'Home player {home_player_id} does not exists'
        )
    home_player = home_player.first()

    away_player = selectors.filter_player_by_id(
        player_id=away_player_id
    )
    if not away_player.exists():
        raise Exception(
            f'Home player {home_player_id} does not exists'
        )
    away_player = away_player.first()

    league = selectors.filter_league_by_id(league_id=league_id)
    if not league.exists():
        raise Exception(
            f'league {league_id} does not exists'
        )
    league = league.first()

    if not status:
        status = GameStatus.DEFAULT.value
    game = Game.objects.create(
        external_id=external_id,
        league=league,
        home_player=home_player,
        away_player=away_player,
        start_dt=start_dt,
        status=status,
        home_score=home_score,
        away_score=away_score,
        line_score=line_score
    )
    update_player_stats_by_game(
        game=game
    )


def _recalculate_players_stats(
    *,
    players_id: List[int]
) -> Union[None]:
    for id_ in players_id:
        statistics.recalculate_player_stats(
            player_id=id_
        )
        predictions_services.recalculate_prediction_stats(
            player_id=id_
        )


def update_game(
    *,
    game: Game,
    status: int,
    home_score: int,
    away_score: int,
    line_score: Dict[str, Any],
    start_dt: Optional[datetime] = None,
    home_player: Optional[Player] = None,
    away_player: Optional[Player] = None
) -> Union[None]:
    """
    update game.
    NOTE: when home_player o away_player are changed,
    player (old and new) stats mush be recalculate
    """
    old_status = GameStatus(game.status)
    new_status = GameStatus(status)
    game.status = status

    h_id = game.h_id
    a_id = game.a_id
    if start_dt:
        game.start_dt = start_dt
    if home_player:
        game.home_player = home_player
    if away_player:
        game.away_player = away_player
    game.home_score = home_score
    game.away_score = away_score
    game.line_score = line_score
    game.save()
    if old_status != new_status and \
            new_status == GameStatus.FINISHED:
        update_player_stats_by_game(game=game)
    predictions_services.update_prediction_by_game_updated(
        game=game
    )
    players_id = []
    if home_player:
        players_id.append(h_id)
        players_id.append(home_player.id)
    if away_player:
        players_id.append(a_id)
        players_id.append(away_player.id)
    if players_id:
        _recalculate_players_stats(
            players_id=players_id
        )


def get_h2h_games_data(
    *,
    h_player_id: int,
    a_player_id: int,
    limit: Optional[int] = None
) -> Union[Dict[str, Any], None]:
    """
    get h2h games data
    Attrs:
        h_player_id: home player id
        a_player_id: away player id
    """
    games_data = statistics.get_games_stats(
        h2h_players_id=[h_player_id, a_player_id],
        status=GameStatus.FINISHED.value,
        limit=limit
    )
    h2h_home_wins = 0
    h2h_away_wins = 0
    for game in games_data:
        start_dt = game['start_dt']
        game['start_dt'] = start_dt.date()
        winner_id = game['winner_id']
        if winner_id == h_player_id:
            h2h_home_wins += 1
            continue
        h2h_away_wins += 1

    data = dict(
        home_wins=h2h_home_wins,
        away_wins=h2h_away_wins,
        games=games_data
    )
    return data


def get_games_data_to_predict(
    *,
    game_id: Optional[int] = None,
    start_dt: Optional[date] = None,
    status: Optional[int] = None,
    min_t_games: Optional[int] = None,
    h2h_games_limit: Optional[int] = None,
    last_games_limit: Optional[int] = None,
    last_games_from_dt: Optional[date] = None,
    filter_: Optional[Dict[str, any]] = None
) -> List[Dict[str, Any]]:
    """
    get games data to predict
    Attrs:
        game_id:  game identification
        start_dt: game start date
        status: status of game (default SCHEDULED)
        min_t_games: min total games of player to predict
        last_games_limit: player last games limit
        last_games_from_dt: player last games from date
        filter_: additional filters
    Return: list of dict(
        id: game identification
        external_id: game external_id
        start_dt: game start_dt
        status: game status
        home_player: home player data
                     (statistics.get_player_stats_data)
        away_player: away player data
                     (statistics.get_player_stats_data)
        h2h_games_data: h2h games data (get_h2h_games_data)
        h_last_games: list of home last games
                      (statistics.get_games_stats)
        a_last_games: list of away last games
                      (statistics.get_games_stats)
    )
    """
    filter_ = filter_ or dict()
    if min_t_games:
        filter_.update(
            home_player__stats__total_games__gte=min_t_games,
            away_player__stats__total_games__gte=min_t_games
        )
    games_qry = selectors.filter_games(
        game_id=game_id,
        start_dt=start_dt,
        status=status,
        filter_=filter_
    ).values(
        'id',
        'external_id',
        'start_dt',
        'status',
        'home_player_id',
        'away_player_id',
    ).order_by('id').distinct('id')
    games_data = []
    for game in games_qry:
        id_ = game['id']
        start_dt_ = game['start_dt']
        h_id = game['home_player_id']
        a_id = game['away_player_id']
        p_stats = statistics.get_player_stats_data(
            player_id=[h_id, a_id]
        )
        home_player = [s for s in p_stats if s['player_id'] == h_id][0]
        away_player = [s for s in p_stats if s['player_id'] == a_id][0]

        h2h_games_data = get_h2h_games_data(
            h_player_id=h_id,
            a_player_id=a_id,
            limit=h2h_games_limit
        )
        h_last_games = statistics.get_last_player_games_data(
            player_id=h_id,
            limit=last_games_limit
        )
        a_last_games = statistics.get_last_player_games_data(
            player_id=a_id,
            from_dt=last_games_from_dt,
            to_dt=start_dt_,
            limit=last_games_limit
        )
        data = dict(
            id=id_,
            external_id=game['external_id'],
            start_dt=start_dt_,
            status=game['status'],
            home_player=home_player,
            away_player=away_player,
            h2h_games_data=h2h_games_data,
            h_last_games=h_last_games,
            a_last_games=a_last_games
        )
        games_data.append(data)
    return games_data
