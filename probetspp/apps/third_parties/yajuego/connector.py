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
        return now.today()
    return None


class YaJuegoConnector:
    def __init__(self):
        self.driver = webdriver.Chrome(DRIVER_PATH)
        self.content = None

    def get_odds_by_league_name(
        self,
        *,
        name: str
    ) -> Union[List[Dict[str, Any]], None]:
        if name not in URL_LEAGUES:
            return None
        url = URL_LEAGUES[name]
        self.driver.get(url)
        # wait a page has been loaded
        WebDriverWait(self.driver, 90).until(
            ec.presence_of_element_located((By.CLASS_NAME, "sports-table"))
        )
        self.content = self.driver.page_source
        self.driver.close()
        return self._read_odds_by_content()

    def _read_odds_by_content(self) -> Union[List[Dict[str, Any]], None]:
        """
        read odds by content
        Attrs:
            content: content of web

        :return:
        """
        soup = BeautifulSoup(self.content, features='html.parser')
        date_ = soup.find(
            'div', class_='sports-head__date'
        ).find('span').text
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
            ).find('span').text
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
                date_=date_,
                time_=time_,
                h_name=h_name,
                a_name=a_name,
                h_odds=h_odds,
                a_odds=a_odds
            ))
        return events_info
