import pathlib
import platform
from enum import Enum
from datetime import datetime
from typing import Union, Dict, Any, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from apps.core.constants import GenderConstants
from apps.flashscore.constants import GenderLeague


_URL = 'https://www.flashscore.co'


class SPORTS(Enum):
    SOCCER = 'futbol'
    BASKET_BALL = 'baloncesto'
    TENNIS = 'tenis'
    TABLE_TENNIS = 'tenis-de-mesa'


class URLS(Enum):
    SPORTS_EVENTS = f'{_URL}/{0}'
    EVENT_DETAIL = f'{_URL}/partido/{0}/'
    TEAM_DETAIL = f'{_URL}/equipo/{0}/'
    PLAYER_DETAIL = f'{_URL}/jugador/{0}/'


class FlashConnector:
    def __init__(self):
        os_name = platform.system()
        main_path = pathlib.Path().absolute()
        driver_path = f'{main_path}' \
                      f'/probetspp/web_drivers/{os_name}/chromedriver'
        self.driver = webdriver.Chrome(driver_path)
        self.content = None

    def get_sports_events(
        self,
        *,
        sport: SPORTS
    ):
        url = URLS.SPORTS_EVENTS.value.format(
            sport.value
        )
        self.driver.get(url)
        # wait a page has been loaded
        WebDriverWait(self.driver, 60).until(
            ec.presence_of_element_located((By.CLASS_NAME, "sportName"))
        )
        self.content = self.driver.page_source

    def _read_events(self) -> Union[None, List[Dict[str, Any]]]:
        """
        read events
        Return: dict of data
        """

        soup = BeautifulSoup(self.content, features='html.parser')
        result = soup.find("div", {"id": "live-table"})
        now = datetime.now()
        date_dt = result.find('div', class_='calendar__datepicker')
        start_dt = f"{date_dt.text.split(' ')[0]}/{now.year}"

        events = result.find_all('div', class_='sportName')
        league = None
        gender = None
        events_info = []
        if not events:
            return
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
                home_player = child.find(
                    'div', class_='event__participant--home'
                ).text
                away_player = child.find(
                    'div', class_='event__participant--away'
                ).text
                score_home = child.find('div',
                                        class_='event__score--home').text
                score_away = child.find('div',
                                        class_='event__score--away').text

                parts = child.find_all('div', class_='event__part')
                line_score = []
                for i in range(1, 6):
                    parts_ = [a for a in parts
                              if f'event__part--{i}' in a.attrs['class']]
                    if not parts_:
                        continue
                    home_ = [e for e in parts_
                             if 'event__part--home' in e.attrs['class']]
                    away_ = [e for e in parts_
                             if 'event__part--away' in e.attrs['class']]
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
