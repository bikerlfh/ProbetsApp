from decimal import Decimal
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Union


class PlayerStatsData:
    def __init__(
        self,
        id: int,
        player_id: int,
        t_games: int,
        w_games: int,
        l_games: int,
        w_sets: int,
        l_sets: int,
        w_points: int,
        l_points: int,
        b2w: int,
        b2l: int,
        g_sold: int,
        t_predictions: int,
        w_predictions: int,
        l_predictions: int,
        cp: Decimal,
        name: Optional[str] = None,
    ):
        self.id = id,
        self.player_id = player_id
        self.name = name
        self.t_games = t_games
        self.w_games = w_games
        self.l_games = l_games
        self.w_sets = w_sets
        self.l_sets = l_sets
        self.w_points = w_points
        self.l_points = l_points
        self.b2w = b2w
        self.b2l = b2l
        self.g_sold = g_sold
        self.t_predictions = t_predictions
        self.w_predictions = w_predictions
        self.l_predictions = l_predictions
        self.cp = cp


class GameStatsData:
    def __init__(
        self,
        id: int,
        status: int,
        start_at: datetime,
        league_id: int,
        h_id: int,
        a_id: int,
        h_score: int,
        a_score: int,
        l_score: int,
        winner_id: int,
        num_set: int,
        h_points: int,
        h_b2w: int,
        a_points: int,
        a_b2w: int,
    ):
        self.id = id
        self.status = status
        self.start_at = start_at
        self.h_id = h_id
        self.a_id = a_id
        self.h_score = h_score
        self.a_score = a_score
        self.l_score = l_score
        self.league_id = league_id
        self.winner_id = winner_id
        self.num_set = num_set
        self.h_points = h_points
        self.h_b2w = h_b2w
        self.a_points = a_points
        self.a_b2w = a_b2w


class H2HData:
    def __init__(
        self,
        home_wins: int,
        away_wins: int,
        games: Optional[List[Dict[str, Any]]] = None
    ):
        self.home_wins = home_wins
        self.away_wins = away_wins
        self.games = None
        if games:
            self.games = [GameStatsData(**g) for g in games]


class GamePredictionData:
    def __init__(
        self,
        id: int,
        name: str,
        league: str,
        start_dt: Union[date, datetime],
        h_id: int,
        a_id: int,
        home_player: Dict[str, Any],
        away_player: Dict[str, Any],
        h2h: Dict[str, Any]
    ):
        self.id = id
        self.name = name
        self.league = league
        self.start_dt = start_dt
        self.h_id = h_id
        self.a_id = a_id
        self.home_player = PlayerStatsData(**home_player)
        self.home_player = PlayerStatsData(**away_player)
        self.h2h = H2HData(**h2h)
