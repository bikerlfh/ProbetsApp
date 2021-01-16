from datetime import date
from typing import List, Dict, Any, Optional, Union

import pandas as pd

from apps.games.constants import GameStatus
from apps.games import (
    selectors as games_selectors,
    services as games_services,
    statistics
)


class AdvancePrediction:
    def __init__(
        self,
        *,
        game_id: Optional[int] = None,
        start_dt: Optional[date] = None,
        status: Optional[int] = None
    ):
        self.game_id = game_id
        self.start_at = start_dt or date.today()
        self.status = status or GameStatus.SCHEDULED.value

        self.games_data = self.__get_prediction_data()

    def __get_prediction_data(self):
        games_qry = games_selectors.filter_games(
            game_id=self.game_id,
            start_dt=self.start_at,
            status=self.status,
            filter_=dict(
                home_player__stats__total_games__gte=10,
                away_player__stats__total_games__gte=10,
            )
        ).values(
            'id',
            'external_id',
            'start_dt',
            'status',
            'home_player_id',
            'away_player_id',
        )
        data_lst = []
        for game in games_qry:
            id_ = game['id']
            h_id = game['home_player_id']
            a_id = game['away_player_id']
            p_stats = statistics.get_player_stats_data(
                players_id=[h_id, a_id]
            )
            home_player = [s for s in p_stats if s['player_id'] == h_id][0]
            away_player = [s for s in p_stats if s['player_id'] == a_id][0]

            h2h_games_data = games_services.get_h2h_games_data(
                h_player_id=h_id,
                a_player_id=a_id
            )
            h_last_games = statistics.get_last_player_games_data(
                player_id=h_id,
                limit=20
            )
            a_last_games = statistics.get_last_player_games_data(
                player_id=a_id,
                limit=20
            )
            data = dict(
                id=id_,
                external_id=game['external_id'],
                start_dt=game['start_dt'],
                status=game['status'],
                home_player=home_player,
                away_player=away_player,
                h2h_games_data=h2h_games_data,
                h_last_games=h_last_games,
                a_last_games=a_last_games
            )
            data_lst.append(data)
        return data_lst
