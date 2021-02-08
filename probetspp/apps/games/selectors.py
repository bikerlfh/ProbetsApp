from datetime import date
from typing import Optional, Union, List, Dict, Any
from django.db.models import QuerySet, Q, F, Case, When, IntegerField

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


def get_player_stats_by_player_id(
    *,
    player_id: int
) -> PlayerStats:
    return PlayerStats.objects.get(player_id=player_id)


def get_all_leagues() -> 'QuerySet[League]':
    return League.objects.all()


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
    game_id: Optional[int] = None,
    league_id: Optional[int] = None,
    start_dt: Optional[date] = None,
    status: Optional[Union[List, int]] = None,
    filter_: Optional[Dict[str, any]] = None
) -> 'QuerySet[Game]':
    filter_ = filter_ or dict()
    if game_id:
        filter_.update(id=game_id)
    if league_id:
        filter_.update(league_id=league_id)
    if start_dt:
        filter_.update(start_dt__date=start_dt)
    if isinstance(status, list):
        filter_.update(status__in=status)
    if isinstance(status, int):
        filter_.update(status=status)
    return Game.objects.filter(**filter_).order_by('start_dt')


def filter_games_by_player_id(
    *,
    player_id: int
) -> 'QuerySet[Game]':
    return Game.objects.filter(
        Q(home_player_id=player_id)
        | Q(away_player_id=player_id)
    ).order_by('-id', '-start_dt')


def filter_player_stats_data(
    *,
    player_id: Optional[Union[int, List[int]]] = None
) -> 'QuerySet[Dict[str, Any]]':
    """
    filter player stats data
    Attrs:
        player_id: player identifier or list ids
    Returns: QuerySet[Dict](
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
    stats_qry = PlayerStats.objects.all().annotate(
        t_games=F('total_games'), w_games=F('won_games'),
        l_games=F('lost_games'), w_sets=F('won_sets'),
        l_sets=F('lost_sets'), w_points=F('won_points'),
        l_points=F('lost_points'), b2w=F('back_to_win'),
        b2l=F('back_to_lose'), g_sold=F('games_sold'),
        t_predictions=F('total_predictions'),
        w_predictions=F('won_predictions'),
        l_predictions=F('lost_predictions'),
        cp=F('confidence_percentage')
    ).values(
        'id', 'player_id', 't_games', 'w_games', 'l_games',
        'w_sets', 'l_sets', 'w_points', 'l_points', 'b2w',
        'b2l', 'g_sold', 't_predictions', 'w_predictions',
        'l_predictions', 'cp'
    )
    if isinstance(player_id, int):
        stats_qry = stats_qry.filter(player_id=player_id)
    elif isinstance(player_id, list):
        stats_qry = stats_qry.filter(player_id__in=player_id)
    return stats_qry


def filter_game_stats_data(
    *,
    game_id: Optional[Union[int, List]] = None,
    player_id: Optional[int] = None,
    league_id: Optional[int] = None,
    status: Optional[Union[int, List]] = None,
    start_dt: Optional[date] = None,
    h2h_players_id: Optional[List[int]] = None,
    filter_: Optional[Dict[str, Any]] = None
) -> 'QuerySet[Dict[str, Any]]':
    """
    filter games stats data
    Attrs:
        game_id: game id or list of games id
        player_id: player identifier
        league_id: league identifier
        status: game status
        start_dt: date of game
        h2h_players_id: list of 2 h2h players id
        limit: limits rows
    """
    game_qry = Game.objects.all().annotate(
        h_id=F('home_player_id'),
        a_id=F('away_player_id'),
        h_name=F('home_player__name'),
        a_name=F('away_player__name'),
        h_score=F('home_score'),
        a_score=F('away_score'),
        l_score=F('line_score'),
        winner_id=Case(
            When(
                home_score__gt=F('away_score'),
                then=F('home_player_id')
            ),
            When(
                home_score__lt=F('away_score'),
                then=F('away_player_id')
            ),
            output_field=IntegerField()
        )
    ).values(
        'id', 'status', 'league_id', 'start_dt',
        'h_id', 'a_id', 'h_name', 'a_name', 'h_score', 'a_score',
        'l_score', 'winner_id'
    ).order_by('-id', '-start_dt')
    filter_ = filter_ or {}
    if isinstance(game_id, list):
        filter_.update(id__in=game_id)
    elif isinstance(game_id, int):
        filter_.update(id=game_id)
    if isinstance(status, int):
        filter_.update(status=status)
    elif isinstance(status, list):
        filter_.update(status__in=status)
    if league_id:
        filter_.update(league_id=league_id)
    if start_dt:
        filter_.update(start_dt__date=start_dt)
    if filter_:
        game_qry = game_qry.filter(**filter_)
    if player_id:
        game_qry = game_qry.filter(
            Q(home_player_id=player_id)
            | Q(away_player_id=player_id)
        )
    elif h2h_players_id and len(h2h_players_id) == 2:
        player_1 = h2h_players_id[0]
        player_2 = h2h_players_id[1]
        game_qry = game_qry.filter(
            Q(home_player_id=player_1,
              away_player_id=player_2)
            | Q(home_player_id=player_2,
                away_player_id=player_1)
        )
    return game_qry
