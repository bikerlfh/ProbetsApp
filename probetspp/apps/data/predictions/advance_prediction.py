import logging
from decimal import Decimal
from datetime import date, datetime
from typing import Optional, List, Dict, Any, Union
from rest_framework.exceptions import ValidationError
from apps.games.constants import GameStatus
from apps.data.weights import wt_score
from apps.data import selectors

logger = logging.getLogger(__name__)


class AdvancePrediction:
    def __init__(
        self,
        *,
        game_id: Optional[int] = None,
        status: Optional[int] = None,
        start_dt: Optional[date] = None,
        start_dt_range: Optional[List[datetime]] = None
    ):
        self.game_id = game_id
        self.start_at = start_dt
        self.status = status or GameStatus.SCHEDULED.value
        self.start_dt_range = start_dt_range
        self.p_wt_diff = None
        self.h2h_wt_diff = None
        self.lg_wt_diff = None
        self.d_opp_wt_diff = None
        self.game_data = None
        self.games_predictions = []
        self.initialize()

    def initialize(self):
        self.game_data = wt_score.get_games_score_data_to_predict(
            game_id=self.game_id,
            start_dt=self.start_at,
            status=self.status,
            start_dt_range=self.start_dt_range
        )

    def analyze_games_to_predict(self):
        self._get_acceptance_value()
        for game in self.game_data:
            data = self._get_winner(game=game)
            if not data:
                continue
            data.update(**game)
            self.games_predictions.append(data)

    def _get_winner(
        self,
        *,
        game: Dict[str, Any]
    ) -> Union[Dict[str, Any], None]:
        """
        get winner
        Attrs:
            game: game data
        Return: dict(
            winner: player id
            confidence: confidence percentage
        )
        """
        game_id = game['game_id']
        winner_p = self._analyze_player_score(game)
        winner_h2h = self._analyze_h2h_score(game)
        winner_lg = self._analyze_last_games_score(game)
        winner_d_opp = self._analyze_d_opp_score(game)
        if not winner_p and not winner_h2h and \
           not winner_lg and not winner_d_opp:
            logger.info(
                f'_get_winner :: 4 none {game_id}'
            )
            return None
        if not winner_h2h and not winner_lg and \
           not winner_d_opp:
            logger.info(
                f'_get_winner :: 2 none {game_id}'
            )
            return None
        p_h2h = winner_p == winner_h2h
        h2h_lg = winner_h2h == winner_lg
        h2h_d_opp = winner_h2h == winner_d_opp
        lg_d_opp = winner_lg == winner_d_opp
        if p_h2h and h2h_lg and h2h_d_opp:
            return dict(
                confidence=90,
                winner_id=winner_p
            )
        if h2h_lg and h2h_d_opp:
            return dict(
                confidence=80,
                winner_id=winner_h2h
            )
        if winner_p == winner_d_opp and lg_d_opp:
            return dict(
                confidence=51,
                winner_id=winner_h2h
            )
        return None

    def _analyze_player_score(
        self,
        game: Dict[str, Any]
    ) -> Union[int, None]:
        """
        analyze players score
        Attrs:
            game: game data
        Return: player id winner or None
        if the acceptable values not match
        """
        h_id = game['h_id']
        a_id = game['a_id']
        h_wt_score = game['h_wt_score']
        a_wt_score = game['a_wt_score']
        diff_p_score = _get_diff(h_wt_score, a_wt_score)
        if diff_p_score < self.p_wt_diff:
            return None
        if h_wt_score > a_wt_score:
            return h_id
        return a_id

    def _analyze_h2h_score(
        self,
        game: Dict[str, Any]
    ) -> Union[int, None]:
        """
        analyze players score
        Attrs:
            game: game data
        Return: player id winner or None
        if the acceptable values not match
        """
        h_id = game['h_id']
        a_id = game['a_id']
        t_h2h = game['t_h2h']
        h_h2h_wt_score = game['h_h2h_wt_score']
        a_h2h_wt_score = game['a_h2h_wt_score']
        diff_h2h_score = _get_diff(h_h2h_wt_score, a_h2h_wt_score)
        if t_h2h < 5 or diff_h2h_score < self.h2h_wt_diff:
            return None
        if h_h2h_wt_score > a_h2h_wt_score:
            return h_id
        return a_id

    def _analyze_last_games_score(
        self,
        game: Dict[str, Any]
    ) -> Union[int, None]:
        """
        analyze players score
        Attrs:
            game: game data
        Return: player id winner or None
        if the acceptable values not match
        """
        h_id = game['h_id']
        a_id = game['a_id']
        h_lg_wt_score = game['h_lg_wt_score']
        a_lg_wt_score = game['a_lg_wt_score']
        diff_lg_score = _get_diff(h_lg_wt_score, a_lg_wt_score)
        if diff_lg_score < self.lg_wt_diff:
            return None
        if h_lg_wt_score > a_lg_wt_score:
            return h_id
        return a_id

    def _analyze_d_opp_score(
        self,
        game: Dict[str, Any]
    ) -> Union[int, None]:
        """
        analyze direct opponents score
        Attrs:
            game: game data
        Return: player id winner or None
        if the acceptable values not match
        """
        h_id = game['h_id']
        a_id = game['a_id']
        h_d_opp_wt_score = game['h_d_opp_wt_score']
        a_d_opp_wt_score = game['a_d_opp_wt_score']
        diff_d_opp_score = _get_diff(h_d_opp_wt_score, a_d_opp_wt_score)
        if diff_d_opp_score < self.d_opp_wt_diff:
            return None
        if h_d_opp_wt_score > a_d_opp_wt_score:
            return h_id
        return a_id

    def _get_acceptance_value(self):
        acc_value_qry = selectors. \
            filter_acceptance_value_active()
        if not acc_value_qry.exists():
            msg = 'acceptance value does not exists'
            logger.error(
                f'AdvancePrediction :: initialize :: {msg}'
            )
            raise ValidationError(msg)
        acc_value = acc_value_qry.first()
        self.p_wt_diff = acc_value['p_wt_diff']
        self.h2h_wt_diff = acc_value['h2h_wt_diff']
        self.lg_wt_diff = acc_value['l_g_wt_diff']
        self.d_opp_wt_diff = acc_value['d_opp_wt_diff']


def _get_diff(
    first_score: Decimal,
    second_score: Decimal
) -> Decimal:
    diff = first_score - second_score
    if first_score < second_score:
        diff = second_score - first_score
    return diff
