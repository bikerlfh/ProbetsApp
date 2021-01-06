import pathlib
import logging
from datetime import datetime, date
from typing import Union, Dict, Any, List, TextIO, Optional

from django.db import transaction

from bs4 import BeautifulSoup
from selenium import webdriver

from apps.core.constants import GenderConstants
from apps.games.constants import GameStatus
from apps.games import (
    selectors as games_selectors,
    services as games_services
)
from apps.flashscore.constants import (
    TABLE_TENNIS_TODAY_URL,
    TableTennisStatus,
    GenderLeague,
    FOLDER_PATH_FLASH_DATA,
    FILENAME_FORMAT_FLASH_DATA
)


logger = logging.getLogger(__name__)


def read_events_web_driver() -> Union[None, List[Dict[str, Any]]]:
    now = datetime.now()
    main_path = pathlib.Path().absolute()
    driver_path = f'{main_path}' \
                  f'/probetspp/web_drivers/chromedriver'
    driver = webdriver.Chrome(driver_path)
    driver.get(TABLE_TENNIS_TODAY_URL)
    driver.implicitly_wait(40)
    content = driver.page_source
    filename = f'{FOLDER_PATH_FLASH_DATA}' \
               f'{now.strftime(FILENAME_FORMAT_FLASH_DATA)}'
    f = open(filename, "w")
    f.write(content)
    f.close()
    data = None
    try:
        data = _read_events(
            content=content,
            event_date=now.date()
        )
    except Exception as exc:
        logger.exception(
            f'read_events_web_driver :: {exc}'
        )
    driver.close()
    return data


def read_events_from_html_file(
    *,
    file_date: date
) -> Union[None, List[Dict[str, Any]]]:
    filename = file_date.strftime(FILENAME_FORMAT_FLASH_DATA)
    file_path = f'{FOLDER_PATH_FLASH_DATA}' \
                f'{filename}'
    file = open(file_path)
    data = None
    try:
        data = _read_events(
            content=file,
            event_date=file_date
        )
    except Exception as exc:
        logger.exception(
            f'read_events_from_html_file :: {exc}'
        )
    file.close()
    return data


def _read_events(
    *,
    content: Union[str, TextIO],
    event_date: Optional[date] = None
) -> Union[None, List[Dict[str, Any]]]:
    """
    read events from flashscore
    :return:
    """
    soup = BeautifulSoup(content, features='html.parser')
    result = soup.find("div", {"id": "live-table"})
    # now = datetime.now()
    # date_dt = result.find('div', class_='calendar__datepicker')
    # start_dt = f"{date_dt.text.split(' ')[0]}/{now.year}"
    start_dt = event_date.strftime('%d/%m/%Y')

    events = result.find_all('div', class_='sportName')
    league = None
    gender = None
    events_info = []
    for child in events[0].children:
        attrs = child.attrs
        if 'event__header' in attrs['class']:
            event_type = child.find('span', class_='event__title--type')
            event_title = child.find('span', class_='event__title--name')
            if GenderLeague.FEMALE.value in event_type.text:
                gender = GenderConstants.FEMALE
            else:
                gender = GenderConstants.MALE
            league = event_title.text
            continue
        if 'event__match' in attrs['class']:
            start_dt_ = start_dt
            start_dt_format = '%d/%m/%Y'
            external_id = attrs['id']
            stage = child.find('div', class_='event__stage--block')
            if stage:
                stage = stage.text
            time = child.find('div', class_='event__time')
            if time:
                start_dt_ = f"{start_dt_} {time.text.replace('SRF', '')}"
                start_dt_format = '%d/%m/%Y %H:%M'
            start_dt_ = datetime.strptime(start_dt_, start_dt_format)
            home_player = child.find('div', class_='event__participant--home').text
            away_player = child.find('div', class_='event__participant--away').text
            score_home = child.find('div', class_='event__score--home').text
            score_away = child.find('div', class_='event__score--away').text

            parts = child.find_all('div', class_='event__part')
            line_score = []
            for i in range(1, 6):
                parts_ = [a for a in parts if f'event__part--{i}' in a.attrs['class']]
                if not parts_:
                    continue
                home_ = [e for e in parts_ if 'event__part--home' in e.attrs['class']]
                away_ = [e for e in parts_ if 'event__part--away' in e.attrs['class']]
                line_score.append({
                    'home': int(home_[0].text),
                    'away': int(away_[0].text)
                })

            events_info.append(
                dict(
                    league=league,
                    gender=gender,
                    external_id=external_id,
                    stage=stage,
                    start_dt=start_dt_,
                    home_player=home_player,
                    away_player=away_player,
                    home_score=int(score_home.replace('-', '0')),
                    away_score=int(score_away.replace('-', '0')),
                    line_score=line_score
                )
            )
    return events_info


@transaction.atomic()
def create_or_update_game(
    *,
    external_id: str,
    h_player_external_id: str,
    a_player_external_id: str,
    start_dt: datetime,
    stage: str,
    gender: int,
    league_external_id: str,
    home_score: int,
    away_score: int,
    line_score: Dict[str, Any]
) -> Union[bool, None]:
    """
    create or update game include league and players
    Attrs:
        external_id: game external_id
        h_player_external_id: home player external id
        a_player_external_id: away player external id
        start_dt: game start at
        stage: stage
        gender: gender league
        league_external_id: league external id
        home_score: home score
        away_score: away score
        line_score: line score
    Returns: bool
        1 - created
        2 - updated
        None
    """
    league_qry = games_selectors.filter_league_by_external_id(
        external_id=league_external_id,
        gender=gender
    )
    league = league_qry.first()
    if not league:
        league = games_services.create_league(
            external_id=league_external_id,
            name=league_external_id,
            gender=gender
        )

    home_player_qry = games_selectors.filter_player_by_external_id(
        external_id=h_player_external_id
    )
    home_player = home_player_qry.first()
    if not home_player:
        home_player = games_services.create_player(
            external_id=h_player_external_id,
            short_name=None,
            name=h_player_external_id,
            gender=gender
        )

    away_player_qry = games_selectors.filter_player_by_external_id(
        external_id=a_player_external_id
    )
    away_player = away_player_qry.first()
    if not away_player:
        away_player = games_services.create_player(
            external_id=a_player_external_id,
            short_name=None,
            name=a_player_external_id,
            gender=gender
        )

    status = GameStatus.SCHEDULED.value
    finished = TableTennisStatus.FINISHED.value
    canceled = TableTennisStatus.CANCELED.value
    in_live = TableTennisStatus.IN_LIVE.value
    if stage and finished in stage:
        status = GameStatus.FINISHED.value
    if stage and canceled in stage:
        status = GameStatus.CANCELED.value
    if stage and in_live in stage:
        status = GameStatus.IN_LIVE.value

    game_qry = games_selectors.filter_game_by_external_id(
        external_id=external_id
    )
    if not game_qry.exists():
        games_services.create_game(
            external_id=external_id,
            home_player_id=home_player.id,
            away_player_id=away_player.id,
            league_id=league.id,
            start_dt=start_dt,
            home_score=home_score,
            away_score=away_score,
            line_score=line_score,
            status=status
        )
        logger.info('create_update_game :: game created')
        return True

    games_services.update_game(
        game=game_qry.first(),
        status=status,
        # start_dt=start_dt,
        home_score=home_score,
        away_score=away_score,
        line_score=line_score,
    )
    logger.info('create_update_game :: game update')
    return False


def load_events(
    *,
    file_date: Optional[date] = None
) -> Union[Dict[str, Any], None]:
    if not file_date:
        events = read_events_web_driver()
    else:
        events = read_events_from_html_file(
            file_date=file_date
        )
    events_created = 0
    events_updated = 0
    for event in events:
        gender = event['gender']
        league = event['league']
        external_id = event['external_id']
        stage = event['stage']
        start_dt = event['start_dt']
        home_player = event['home_player']
        away_player = event['away_player']
        home_score = event['home_score']
        away_score = event['away_score']
        line_score = event['line_score']

        created = create_or_update_game(
            external_id=external_id,
            h_player_external_id=home_player,
            a_player_external_id=away_player,
            start_dt=start_dt,
            stage=stage,
            gender=gender.value,
            league_external_id=league,
            home_score=home_score,
            away_score=away_score,
            line_score=line_score
        )
        events_created += 1 if created else 0
        events_updated += 1 if created is False else 0
    data = dict(
        events_created=events_created,
        events_updated=events_updated
    )
    return data
