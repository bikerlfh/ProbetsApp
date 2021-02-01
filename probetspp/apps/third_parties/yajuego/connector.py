import re
import logging
from typing import Dict, Union, List, Any
from datetime import datetime, date
from babel.dates import format_date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from apps.utils.constants import DRIVER_PATH
from apps.third_parties.yajuego.constants import URL_LEAGUES


logger = logging.getLogger(__name__)


def _validate_today_date(date_: str) -> Union[date, None]:
    now = datetime.now()
    now_ = format_date(now, "EEE d MMM", locale='es')
    now_ = re.sub(r"\.", "", now_)
    if now_ == date_:
        return now.today().date()
    return None


class YaJuegoConnector:
    def __init__(self):
        self.driver = None
        self.content = None
        self.odds = []

    def get_odds_by_leagues(
        self,
        *,
        leagues_data: List[Dict[str, Any]]
    ) -> Union[List[Dict[str, Any]], None]:
        """
        get odds by league name
        Attrs:
            names: list of league names
        Returns: None or list of dict(
            date_: date of game
            time_: time of game
            h_name: home player name
            a_name: away player name
            h_odds: home player odds
            a_odds: away player odds
        )
        """
        self.driver = webdriver.Chrome(DRIVER_PATH)
        for league_ in leagues_data:
            league_id = league_['id']
            name = league_['name']
            if name not in URL_LEAGUES:
                continue
            url = URL_LEAGUES[name]
            self.driver.get(url)
            # wait a page has been loaded
            try:
                # find sports-table or search-results(no events)
                or_ = "//*[contains(@class,'sports-table') or " \
                      "(contains(@class,'search-results'))]"
                WebDriverWait(self.driver, 60).until(
                    ec.presence_of_all_elements_located((By.XPATH, or_)),
                )
            except Exception as exc:
                logger.exception(f'get_odds_by_league_name :: {exc}')
                return None
            last_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            while True:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight);"
                )
                new_height = self.driver.execute_script(
                    "return document.body.scrollHeight"
                )
                if new_height == last_height:
                    break
                last_height = new_height
            self.content = self.driver.page_source
            odds = self._read_odds_by_content(
                league_id=league_id
            )
            if not odds:
                continue
            self.odds += odds
        self.driver.close()
        return self.odds

    def _read_odds_by_content(
        self,
        league_id: int
    ) -> Union[List[Dict[str, Any]], None]:
        """
        read odds by content
        Attrs:
            content: content of web

        Returns: None or list of dict(
            date_: date of game
            time_: time of game
            h_name: home player name
            a_name: away player name
            h_odds: home player odds
            a_odds: away player odds
        )
        """
        soup = BeautifulSoup(self.content, features='html.parser')
        search_result = soup.find('div', class_='search-results')
        if search_result:
            no_events = search_result.text.lower()
            if 'no hay mercados' in no_events:
                return None

        date_ = soup.find(
            'div', class_='sports-head__date'
        ).text
        date_ = _validate_today_date(date_)
        if not date_:
            return
        result = soup.find("div", {"class": "sports-table"})
        events = result.find_all('div', class_='table-f')
        events_info = []
        if not events:
            return
        for child in events:
            time_ = child.find(
                'div', class_='sports-table__time'
            )
            # if game is in live
            if not time_:
                continue
            time_ = time_.text
            h_name = child.find(
                'div', class_='sports-table__home'
            ).text
            a_name = child.find(
                'div', class_='sports-table__away'
            ).text
            odds = child.find_all(
                'li', class_='sports-table__odds-item'
            )
            h_odds = None
            a_odds = None
            for odd in odds:
                p_odd = odd.find(
                    'div',
                    class_='sports-table__odds-num'
                ).text
                p_name = odd.find(
                    'div',
                    class_='sports-table__odds-team'
                ).text
                if p_name == h_name:
                    h_odds = p_odd
                    continue
                a_odds = p_odd
            events_info.append(dict(
                league_id=league_id,
                date=date_,
                time=time_,
                h_name=h_name,
                a_name=a_name,
                h_odds=h_odds,
                a_odds=a_odds
            ))
        return events_info
