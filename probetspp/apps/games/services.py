import logging
from datetime import datetime, date
from typing import Union, Optional, Dict, Any
from django.db.models import F

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
    home_player_id = game.home_player.id
    away_player_id = game.away_player.id

    status = GameStatus(game.status)
    if status != GameStatus.FINISHED:
        return

    game_stats = statistics.get_game_stats(game=game)
    is_home_winner = game.is_winner(home_player_id)
    home_stats = selectors.get_player_stats(
        player_id=home_player_id
    )
    away_stats = selectors.get_player_stats(
        player_id=away_player_id
    )
    home_stats.total_games += 1
    away_stats.total_games += 1
    if is_home_winner:
        home_stats.won_games += 1
        away_stats.lost_games += 1
    else:
        away_stats.won_games += 1
        home_stats.lost_games += 1

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

    h_back_to_win = game_stats['h_back_to_win']
    a_back_to_win = game_stats['a_back_to_win']
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


def update_game(
    *,
    game: Game,
    status: int,
    home_score: int,
    away_score: int,
    line_score: Dict[str, Any],
    start_dt: Optional[datetime] = None,
) -> Union[None]:
    old_status = GameStatus(game.status)
    new_status = GameStatus(status)
    game.status = status
    if start_dt:
        game.start_dt = start_dt
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


def get_games(
    *,
    start_dt: date,
    league_id: Optional[int] = None,
    status: Optional[int] = None
) -> Dict[str, Any]:
    data = selectors.filter_games(
        league_id=league_id,
        start_dt=start_dt,
        status=status
    ).annotate(
        home_name=F('home_player__name'),
        away_name=F('away_player__name')
    ).values(
        'id',
        'status',
        'start_dt',
        'league_id',
        'home_player_id',
        'home_name',
        'away_player_id',
        'away_name',
        'home_score',
        'away_score',
        'line_score'
    )
    for game in data:
        name = f"{game['home_name']} vs {game['away_name']}"
        game.update(
            name=name,
            home_player=dict(
                id=game['home_player_id'],
                name=game['home_name']
            ),
            away_player=dict(
                id=game['away_player_id'],
                name=game['away_name']
            )
        )
        game.pop('home_player_id')
        game.pop('home_name')
        game.pop('away_player_id')
        game.pop('away_name')
    return data


def _get_h2h_data(
    *,
    home_player_id: int,
    away_player_id: int
) -> Dict[str, Any]:
    h2h_games_qry = selectors.filter_h2h_games(
        first_player_id=home_player_id,
        second_player_id=away_player_id,
        status=GameStatus.FINISHED.value
    )
    games = []
    h2h_home_wins = 0
    h2h_away_wins = 0
    for game in h2h_games_qry:
        games.append(dict(
            id=game.id,
            start_dt=game.start_dt.date(),
            status=game.status,
            league_id=game.league_id,
            home_player_id=game.home_player_id,
            away_player_id=game.away_player_id,
            home_score=game.home_score,
            away_score=game.away_score,
            line_score=game.line_score
        ))
        is_home_winner = game.is_winner(
            player_id=home_player_id
        )
        if is_home_winner:
            h2h_home_wins += 1
        else:
            h2h_away_wins += 1

    data = dict(
        home_wins=h2h_home_wins,
        away_wins=h2h_away_wins,
        games=games
    )
    return data


def get_game_data_to_prediction(
    *,
    game: Game
) -> Dict[str, Any]:
    home_player = game.home_player
    away_player = game.away_player
    h2h_data = _get_h2h_data(
        home_player_id=home_player.id,
        away_player_id=away_player.id
    )
    data = dict(
        id=game.id,
        name=f'{str(home_player)} vs {str(away_player)}',
        league=str(game.league),
        start_dt=game.start_dt,
        home_player_id=home_player.id,
        away_player_id=away_player.id,
        h2h=h2h_data
    )
    home_data = statistics.get_player_stats_data(
        player=home_player
    )
    data.update(home_player=home_data)
    away_data = statistics.get_player_stats_data(
        player=away_player
    )
    data.update(away_player=away_data)
    return data
