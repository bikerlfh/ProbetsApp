from datetime import date, datetime
from typing import Optional, Union, List
from django.db.models import QuerySet, Q

from apps.games.constants import GameStatus
from apps.games.models import (
    League,
    Game,
    Player,
    PlayerStats
)


def filter_player(
    *,
    player_id: Optional[int] = None,
    external_id: Optional[str] = None,
    league_id: Optional[int] = None
) -> 'QuerySet[Player]':
    player_qry = Player.objects.all()
    filter_ = {}
    if player_id:
        filter_.update(id=player_id)
    if external_id:
        filter_.update(external_id=external_id)
    if league_id:
        player_qry = player_qry.filter(
            Q(home_games__league_id=league_id)
            | Q(away_games__league_id=league_id)
        )
    if filter_:
        player_qry = player_qry.filter(**filter_)
    return player_qry


def filter_player_by_id(
    *,
    player_id: int
) -> 'QuerySet[Player]':
    return filter_player(player_id=player_id)


def filter_player_by_external_id(
    *,
    external_id: str
) -> 'QuerySet[Player]':
    return filter_player(external_id=external_id)


def get_player_stats(
    *,
    player_id: int
) -> PlayerStats:
    return PlayerStats.objects.get(player_id=player_id)


def filter_league_by_id(
    *,
    league_id: int
) -> 'QuerySet[League]':
    return League.objects.filter(id=league_id)


def filter_league_by_external_id(
    *,
    external_id: str,
    gender: Optional[int] = None
) -> 'QuerySet[League]':
    filter_ = dict(external_id=external_id)
    if gender is not None:
        filter_.update(gender=gender)
    return League.objects.filter(**filter_)


def get_all_leagues() -> 'QuerySet[League]':
    return League.objects.all()


def filter_game_by_id(
    *,
    game_id: int
) -> 'QuerySet[Game]':
    return Game.objects.filter(id=game_id)


def filter_game_by_external_id(
    *,
    external_id: str
) -> 'QuerySet[Game]':
    return Game.objects.filter(external_id=external_id)


def filter_games(
    *,
    league_id: Optional[int] = None,
    start_dt: Optional[date] = None,
    status: Optional[Union[List, int]] = None
) -> 'QuerySet[Game]':
    filter_ = dict()
    game_qry = Game.objects.all().order_by('start_dt')
    if league_id:
        filter_.update(league_id=league_id)
    if start_dt:
        filter_.update(start_dt__date=start_dt)
    if isinstance(status, list):
        filter_.update(status__in=status)
    if isinstance(status, int):
        filter_.update(status=status)
    if filter_:
        game_qry = game_qry.filter(**filter_)
    return game_qry


def filter_h2h_games(
    *,
    first_player_id: int,
    second_player_id: int,
    status: Optional[Union[List, int]] = None
) -> 'QuerySet[Game]':
    game_qry = Game.objects.filter(
        Q(home_player_id=first_player_id,
          away_player_id=second_player_id)
        | Q(home_player_id=second_player_id,
            away_player_id=first_player_id)
    ).order_by('-start_dt')
    if isinstance(status, list):
        game_qry = game_qry.filter(status__in=status)
    elif isinstance(status, int):
        game_qry = game_qry.filter(status=status)
    return game_qry


def filter_last_games_by_player_id(
    *,
    player_id: int,
    limit: Optional[int] = None
) -> 'QuerySet[Game]':
    now = datetime.now().date()
    game_qry = Game.objects.filter(
        Q(home_player_id=player_id)
        | Q(away_player_id=player_id),
        status=GameStatus.FINISHED.value,
        start_dt__date__lte=now
    ).order_by('-start_dt')
    if limit:
        game_qry = game_qry[:limit]
    return game_qry
