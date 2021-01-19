from datetime import date
from typing import Optional, Dict, Any
from decimal import Decimal

from apps.games.constants import GameStatus
from apps.games import (
    services as games_services
)

from apps.data.constants import MIN_DIFF_PLAYER_SCORE
from apps.data.weights import (
    wt_player,
    wt_h2h,
    wt_games
)


class AdvancePrediction:
    def __init__(
        self,
        *,
        game_id: Optional[int] = None,
        start_dt: Optional[date] = None,
        status: Optional[int] = None,
        min_diff: Optional[Decimal] = MIN_DIFF_PLAYER_SCORE
    ):
        self._game_id = game_id
        self._start_at = start_dt or date.today()
        self._status = status or GameStatus.SCHEDULED.value
        self._games_data = games_services.get_games_data_to_predict(
            game_id=game_id,
            start_dt=start_dt,
            status=status
        )
        self.min_diff = min_diff
        self.game_score_data = []
        self.initialize()

    def initialize(self):
        if not self._games_data:
            return
        for game in self._games_data:
            h_id = game['home_player']['id']
            a_id = game['away_player']['id']
            p_wt_score = wt_player.get_player_scores_by_game(
                h_id=h_id,
                a_id=a_id
            )
            """validate_game_by_wt_player_score(
                game_id=game['id'],
                h_id=h_id,
                a_id=a_id,
                min_diff=self.min_diff
            )"""

            h2h_wt_score = wt_h2h.get_h2h_wt_score(
                h_id=h_id,
                a_id=a_id,
                h2h_data=game['h2h_games_data']
            )
            last_games_wt_score = self._get_last_game_wt_score(game=game)

            d_g_wt_score = wt_games.get_direct_opponents_wt_score(
                h_id=h_id,
                a_id=a_id,
                h_last_games=game['h_last_games'],
                a_last_games=game['a_last_games'],
            )
            data = dict(
                id=game['id'],
                h_id=h_id,
                a_id=a_id,
                **p_wt_score,
                **h2h_wt_score,
                **last_games_wt_score,
                **d_g_wt_score
            )
            self.game_score_data.append(data)

    def _get_last_game_wt_score(
        self,
        game: Dict[str, Any]
    ) -> Dict[str, Any]:
        h_lg_wt_score = wt_games.get_last_games_player_wt_score(
            player_id=game['home_player']['id'],
            games_data=game['h_last_games']
        )
        a_lg_wt_score = wt_games.get_last_games_player_wt_score(
            player_id=game['away_player']['id'],
            games_data=game['a_last_games']
        )
        return dict(
            h_lg_wt_score=h_lg_wt_score,
            a_lg_wt_score=a_lg_wt_score
        )
