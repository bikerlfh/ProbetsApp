import re
import logging
from datetime import datetime
from typing import Union, List, Dict
from django.db.models import F
from django.utils import timezone
from apps.utils import services as utils_services
from apps.core.constants import GenderConstants
from apps.games.constants import GameStatus
from apps.games import selectors as games_selectors
from apps.third_parties.yajuego.connector import YaJuegoConnector


logger = logging.getLogger(__name__)


def _format_league_name(
    *,
    name: str,
    gender: int
) -> Union[str, None]:
    regex = re.compile(r'(\(\w+\))')
    gender = GenderConstants(gender)
    name = regex.sub('', name)
    name = re.sub(r"\s+", "", name).lower()
    if gender == GenderConstants.FEMALE:
        name = f'{name}_women'
    return name


def update_odds_games_by_leagues(
    *,
    leagues_data: List[Dict[str, any]]
) -> Union[None]:
    """
    Attrs:
        leagues_data: list of dict(
            id: league id
            name: league name
            gender: league gender
        )
    Return: None
    """
    for data_ in leagues_data:
        name = _format_league_name(
            name=data_['name'],
            gender=data_['gender']
        )
        if not name:
            continue
        data_.update(name=name)

    connector = YaJuegoConnector()
    odds = connector.get_odds_by_leagues(
        leagues_data=leagues_data
    )
    if not odds:
        return
    c_stext = (lambda x, y: utils_services.get_similarity_text(
        first_text=x,
        second_text=y
    ) >= 0.49)
    c_game = (lambda h1, h2, a1, a2: c_stext(h1, h2) and c_stext(a1, a2))
    now = datetime.now().date()
    games_qry = games_selectors.filter_games(
        start_dt=now,
        status=GameStatus.SCHEDULED.value,
    ).annotate(
        h_name=F('home_player__name'),
        a_name=F('away_player__name'),
    ).values(
        'id',
        'league_id',
        'start_dt',
        'h_name',
        'a_name'
    )
    games = list(games_qry)
    for odds_ in odds:
        h_name = odds_['h_name']
        a_name = odds_['a_name']
        time_ = odds_['time']

        game = None
        for g in games:
            is_valid = c_game(g['h_name'], h_name, g['a_name'], a_name)
            if is_valid:
                game = g
                break
        if not game:
            continue
        g_time = timezone. \
            localtime(game['start_dt']).strftime('%H:%M')

        if g_time != time_:
            continue
        h_odds = odds_['h_odds']
        a_odds = odds_['a_odds']
        game_id = game['id']
        games_selectors.filter_game_by_id(
            game_id=game_id
        ).update(
            h_odds=h_odds,
            a_odds=a_odds
        )
        logger.info(
            f'update_odds_games_by_league_id :: '
            f'odds of game {game_id} has been update'
        )


def update_odds_games() -> Union[None]:
    now = datetime.now().date()
    league_data = games_selectors.get_all_leagues().filter(
        games__status=GameStatus.SCHEDULED.value,
        games__start_dt__date=now
    ).order_by('id').distinct('id').values(
        'id',
        'name',
        'gender'
    )
    update_odds_games_by_leagues(
        leagues_data=league_data
    )
