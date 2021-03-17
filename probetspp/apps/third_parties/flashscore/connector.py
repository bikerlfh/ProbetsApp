from enum import Enum
from datetime import datetime, date
from typing import Union, Dict, Any, List, Optional, TextIO
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from apps.core.constants import GenderConstants
from apps.third_parties.chrome_custom import ChromeCustom
from apps.third_parties.flashscore.constants import GenderLeague


_URL = 'https://www.flashscore.co'


class SPORTS(Enum):
    SOCCER = 'futbol'
    BASKET_BALL = 'baloncesto'
    TENNIS = 'tenis'
    TABLE_TENNIS = 'tenis-de-mesa'


class URLS(Enum):
    SPORT_EVENTS = _URL + '/{}/'
    EVENT_DETAIL = _URL + '/partido/{}/'
    TEAM_DETAIL = _URL + '/equipo/{}/'
    PLAYER_DETAIL = _URL + '/jugador/{}/'


class FlashConnector:
    def __init__(
        self,
        *,
        sport: Optional[SPORTS] = SPORTS.TABLE_TENNIS
    ):
        self.sport = sport.value
        self.driver = ChromeCustom()
        self.content = None
        self.events = None
        self.url = None

    def get_today_events(
        self,
        *,
        sport: Optional[SPORTS] = SPORTS.TABLE_TENNIS
    ) -> List[Dict[str, Any]]:
        """
        get events by sport with odds
        Return: list of dict(
            league: league name
            gender: gender
            external_id: game external id
            stage: stage
            start_dt: start dt
            home_player: home player external id
            away_player: away player external id
            home_score: home score
            away_score: away score
            line_score: dict of line score
            h_odds: home odd
            a_odds: away odd
        )
        """
        self.url = URLS.SPORT_EVENTS.value.format(
            sport.value
        )
        self.content = self.driver.get_content(
            self.url,
            wait_until_method=ec.presence_of_element_located(
                (By.CLASS_NAME, "sportName")
            )
        )
        self.events = FlashConnector.read_events_by_content(
            content=self.content,
            event_date=datetime.now().date()
        )
        if self.events:
            odds_events = self._get_odds_events()
            df_odds = pd.DataFrame(odds_events)
            df_events = pd.DataFrame(self.events)
            df_events['h_odds'] = df_odds[
                df_odds['external_id'] == df_events['external_id']]['h_odds']
            df_events['a_odds'] = df_odds[
                df_odds['external_id'] == df_events['external_id']]['a_odds']
            self.events = df_events.to_dict(orient='records')
        self.driver.close()
        return self.events

    def _get_odds_events(self) -> List[Dict[str, Any]]:
        """
        get odds of today events
        invoke from get_today_events
        Returns: list of dict(
            external_id: game external id
            h_odd: home player odd
            a_odd: away player odd
        )
        """
        data = []
        odds_content = self.driver.get_content_by_xpath_click(
            url=self.url,
            xpath="//div[text()='Cuotas']",
            wait_until_method=[
                ec.presence_of_element_located(
                    (By.CLASS_NAME, "sportName")
                ),
                ec.presence_of_element_located(
                    (By.CLASS_NAME, "event__participant")
                )
            ]
        )
        soup = BeautifulSoup(odds_content, features='html.parser')
        result = soup.find("div", {"id": "live-table"})
        events = result.find_all('div', class_='sportName')
        for child in events[0].children:
            if 'event__match' in child.attrs['class']:
                external_id = child.attrs['id']
                h_odds = None
                a_odds = None
                h_odds_span = child.find(
                    'div', class_='event__odd--odd1'
                ).find('span')
                a_odds_span = child.find(
                    'div', class_='event__odd--odd2'
                ).find('span')
                if h_odds_span:
                    h_odds = h_odds_span.text
                if a_odds_span:
                    a_odds = a_odds_span.text
                data.append(dict(
                    external_id=external_id,
                    h_odds=h_odds,
                    a_odds=a_odds
                ))
        return data

    def get_event_detail(
        self,
        *,
        external_id: str
    ) -> Union[Dict[str, Any], None]:
        url = URLS.EVENT_DETAIL.value.format(
            external_id
        )
        # wait a page has been loaded
        or_ = "//*[contains(@class,'part--current') or " \
              "(contains(@class,'noData')) or (contains(@class,'error'))]"
        content = self.driver.get_content(
            url,
            wait_until_method=ec.presence_of_all_elements_located((
                By.XPATH, or_
            )))
        self.driver.close()
        soup = BeautifulSoup(content, features='html.parser')
        error_ = soup.find('div', class_='error')
        if error_:
            return dict(error=True)
        match_info = soup.select("div[class^=matchInfo]")[0]

        h_score = None
        a_score = None
        for span_ in match_info.select("span"):
            attrs = span_.attrs
            if 'class' not in attrs:
                if not h_score:
                    h_score = span_.text
                    continue
                a_score = span_.text
        if not h_score:
            h_score = '0'
        if not a_score:
            a_score = '0'
        stage = match_info.select("span[class^=detailStatus]")[0].text
        line_score_panel = soup.find("div", class_='table-tennis')
        line_score = []
        if line_score_panel:
            parts = line_score_panel.select("div[class^=part__]")
            for i in range(1, 6):
                score_ = {}
                for part_ in parts:
                    attrs = part_.attrs
                    if 'class' not in attrs:
                        continue
                    is_part = any(a == f'part--{i}' for a in attrs['class'])
                    if not is_part:
                        continue
                    is_home = any(a.startswith('home') for a in attrs['class'])
                    if len(part_.text) == 0:
                        continue
                    if is_home:
                        score_.update(dict(home=part_.text))
                        continue
                    score_.update(dict(away=part_.text))
                if score_:
                    line_score.append(score_)
        data = dict(
            stage=stage,
            home_score=int(h_score.replace('-', '0')),
            away_score=int(a_score.replace('-', '0')),
            line_score=line_score
        )
        return data

    @classmethod
    def read_events_by_content(
        cls,
        *,
        content: Union[str, TextIO],
        event_date: date
    ) -> Union[None, List[Dict[str, Any]]]:
        """
        read events from content web
        Attrs:
            content: content of web
            event_date: event dates
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
        if not events:
            return
        for child in events[0].children:
            attrs = child.attrs
            if 'event__header' in attrs['class']:
                event_type = child.find('span', class_='event__title--type')
                event_title = child.find('span', class_='event__title--name')
                if GenderLeague.FEMALE.value in event_type.text:
                    gender = GenderConstants.FEMALE.value
                else:
                    gender = GenderConstants.MALE.value
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
                score_home = child.find(
                    'div', class_='event__score--home'
                ).text
                score_away = child.find(
                    'div', class_='event__score--away'
                ).text

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
