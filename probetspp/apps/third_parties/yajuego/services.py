import re
import logging
from typing import Union, List, Dict, Any
from apps.games import selectors as games_selectors
from apps.third_parties.yajuego.connector import YaJuegoConnector


logger = logging.getLogger(__name__)


def _format_league_name(
    *,
    league_id: int
) -> Union[str, None]:
    regex = re.compile(r'(\(\w+\))')
    league = games_selectors. \
        filter_league_by_id(league_id=league_id).first()
    if not league:
        msg = 'league does not exists'
        logger.error(f'_get_url :: {msg}')
        return
    name = regex.sub('', league.name)
    name = re.sub(r"\s+", "", name).lower()
    return name


def get_odds_by_league_id(
    *,
    league_id: int
) -> Union[List[Dict[str, Any]], None]:
    league_name = _format_league_name(league_id=league_id)
    if not league_name:
        return None
    connector = YaJuegoConnector()
    odds = connector.get_odds_by_league_name(
        name=league_name
    )
    return odds
