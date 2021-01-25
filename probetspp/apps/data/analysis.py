import logging
from decimal import Decimal
from datetime import date, datetime
from typing import Optional, List, Dict, Any, Union
from rest_framework.exceptions import ValidationError
from apps.data.constants import CONFIDENCE_ALLOWED
from apps.data.weights import wt_score
from apps.data import selectors

logger = logging.getLogger(__name__)


class AdvanceAnalysis:
    """
    Advance Analysis
    """
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
        self.status = status
        self.start_dt_range = start_dt_range
        self.p_wt_diff = None
        self.h2h_wt_diff = None
        self.lg_wt_diff = None
        self.d_opp_wt_diff = None
        # weights to default
        self.wt_player = 0
        self.wt_h2h = 0
        self.wt_last_games = 0
        self.wt_direct_opponents = 0
        self.wt_total = 0

        self.acceptance_value_id = None
        self._game_data = None
        self.games_data = []
        # game data to create predictions
        self.games_to_predict = []
        self.initialize()

    def initialize(self):
        self._load_default_wt()
        self._get_acceptance_value()
        self._game_data = wt_score.get_games_score_data_to_predict(
            game_id=self.game_id,
            start_dt=self.start_at,
            status=self.status,
            start_dt_range=self.start_dt_range,
            last_games_limit=10
        )

    def analyze_games(self):
        """
        analyze games to predict
        """
        for game in self._game_data:
            data = game
            data.update(
                acceptance_value_id=self.acceptance_value_id,
                **self._get_winner(game=game)
            )
            self.games_data.append(data)
            if data['confidence'] >= CONFIDENCE_ALLOWED:
                self.games_to_predict.append(data)

    def _get_winner(
        self,
        *,
        game: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        get winner
        Attrs:
            game: game data
        Return: dict(
            winner: player id
            confidence: confidence percentage
        )
        """
        h_id = game['h_id']
        a_id = game['a_id']
        winner_p = self._analyze_player_score(game)
        winner_h2h = self._analyze_h2h_score(game)
        winner_lg = self._analyze_last_games_score(game)
        winner_d_opp = self._analyze_d_opp_score(game)

        scores = self._get_players_score(game=game)
        h_score = scores.get('h_score')
        a_score = scores.get('a_score')
        winner_id = h_id
        if h_score < a_score:
            winner_id = a_id

        confidence_ = 0
        if winner_id == winner_p:
            confidence_ += self.wt_player
        if winner_id == winner_h2h:
            confidence_ += self.wt_h2h
        if winner_id == winner_lg:
            confidence_ += self.wt_last_games
        if winner_id == winner_d_opp:
            confidence_ += self.wt_direct_opponents

        confidence_ = 100 * (confidence_ / self.wt_total)

        data = dict(
            winner_id=winner_id,
            confidence=confidence_
        )
        return data

    def _get_players_score(
        self,
        game: Dict[str, Any]
    ) -> Dict[str, Any]:
        h_wt_score = game['h_wt_score']
        a_wt_score = game['a_wt_score']
        h_h2h_wt_score = game['h_h2h_wt_score']
        a_h2h_wt_score = game['a_h2h_wt_score']
        h_lg_wt_score = game['h_lg_wt_score']
        a_lg_wt_score = game['a_lg_wt_score']
        h_d_opp_wt_score = game['h_d_opp_wt_score']
        a_d_opp_wt_score = game['a_d_opp_wt_score']

        h_score = h_wt_score + h_h2h_wt_score
        h_score += h_lg_wt_score + h_d_opp_wt_score
        a_score = a_wt_score + a_h2h_wt_score
        a_score += a_lg_wt_score + a_d_opp_wt_score
        return dict(
            h_score=h_score,
            a_score=a_score
        )

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
        self.acceptance_value_id = acc_value['id']
        self.p_wt_diff = acc_value['p_wt_diff']
        self.h2h_wt_diff = acc_value['h2h_wt_diff']
        self.lg_wt_diff = acc_value['lg_wt_diff']
        self.d_opp_wt_diff = acc_value['d_opp_wt_diff']

    def _load_default_wt(self):
        d_ = selectors.filter_default_data_weights().first()
        self.wt_h2h = d_['wt_h2h']
        self.wt_last_games = d_['wt_last_games']
        self.wt_direct_opponents = d_['wt_direct_opponents']
        self.wt_player = d_['wt_games'] + d_['wt_sets'] + d_['wt_points']
        self.wt_player += d_['wt_games_sold'] + d_['wt_predictions']
        self.wt_player = self.wt_player / 5
        self.wt_total = self.wt_h2h + self.wt_last_games
        self.wt_total += self.wt_direct_opponents + self.wt_player


def _get_diff(
    first_score: Decimal,
    second_score: Decimal
) -> Decimal:
    diff = first_score - second_score
    if first_score < second_score:
        diff = second_score - first_score
    return diff
