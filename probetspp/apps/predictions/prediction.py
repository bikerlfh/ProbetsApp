from decimal import Decimal
from typing import Union, Dict, Any

from apps.utils.decimal import format_decimal_to_n_places

from apps.games import selectors as games_selectors

from apps.predictions.constants import (
    NUM_H2H_GAMES_TO_PREDICT,
    ALLOWED_H2H_PERCENTAGE,
    LAST_H2H_GAMES_LIMIT_PREDICTION,
    NUM_LAST_GAMES_TO_PREDICT,
    ALLOWED_PERCENTAGE_LAST_GAMES,
    WinnerPrediction
)


def _is_player_winner(
    *,
    game_data: Dict[str, Any],
    player_id: int
) -> bool:
    home_player_id = game_data['home_player_id']
    away_player_id = game_data['away_player_id']
    home_score = game_data['home_score']
    away_score = game_data['away_score']
    if home_score > away_score:
        return home_player_id == player_id
    return away_player_id == player_id


class BasicPrediction:
    """
    Apply basic prediction from game data
    """
    def __init__(self, game_data: Dict[str, Any]):
        self.game_data = game_data
        self.game_id = self.game_data['id']
        self.league = self.game_data['league']
        self.start_dt = self.game_data['start_dt']
        self.home_player = self.game_data['home_player']
        self.home_player_id = self.home_player['id']
        self.away_player = self.game_data['away_player']
        self.away_player_id = self.away_player['id']
        self.h2h = self.game_data['h2h']

    def get_prediction(self) -> Union[Dict[str, Any], None]:
        last_games_prediction = self.get_last_games_prediction()
        h2h_prediction = self._get_h2h_prediction()
        if h2h_prediction is None or last_games_prediction is None:
            return None

        l_g_prediction = last_games_prediction['prediction']
        l_g_confidence = last_games_prediction['confidence_percentage']
        h2h_prediction_ = h2h_prediction['prediction']
        h2h_confidence = h2h_prediction['confidence_percentage']

        winner_prediction = h2h_prediction_
        if l_g_prediction != h2h_prediction_ and \
                l_g_confidence > h2h_confidence:
            diff = l_g_confidence - h2h_confidence
            if diff > 30:
                winner_prediction = l_g_prediction
        data = dict(
            id=self.game_id,
            name=self.game_data['name'],
            league=self.league,
            start_dt=self.start_dt,
            winner_prediction=winner_prediction,
            last_games_prediction=last_games_prediction,
            h2h_prediction=h2h_prediction,
            home_player=self.home_player,
            away_player=self.away_player,
            h2h=self.h2h
        )
        return data

    def _get_last_games_player_data(
        self,
        *,
        player_id: int
    ) -> Union[Dict[str, Any], None]:
        game_qry = games_selectors.filter_last_games_by_player_id(
            player_id=player_id,
            limit=NUM_LAST_GAMES_TO_PREDICT
        )
        won_games = 0
        lost_games = 0
        total_games = 0
        for game in game_qry:
            total_games += 1
            is_winner = game.is_winner(player_id=player_id)
            if is_winner:
                won_games += 1
                continue
            lost_games += 1

        if total_games <= 0:
            return None
        percentage = 100 * (won_games / total_games)
        data = dict(
            player_id=player_id,
            percentage=percentage,
            won_games=won_games,
            lost_games=lost_games,
            total_games=total_games
        )
        return data

    def get_last_games_prediction(self) -> Union[Dict[str, Any], None]:
        last_home_data = self._get_last_games_player_data(
            player_id=self.home_player_id
        )
        last_away_data = self._get_last_games_player_data(
            player_id=self.away_player_id
        )
        if not last_home_data or not last_away_data:
            return None
        h_total_games = last_home_data['total_games']
        a_total_games = last_away_data['total_games']

        home_percentage = last_home_data['percentage']
        away_percentage = last_away_data['percentage']

        if home_percentage == away_percentage:
            prediction = WinnerPrediction.HOME_OR_AWAY
            confidence_percentage = 50
        elif home_percentage > away_percentage:
            prediction = WinnerPrediction.HOME_PLAYER
            confidence_percentage = home_percentage
        else:
            prediction = WinnerPrediction.AWAY_PLAYER
            confidence_percentage = away_percentage

        if h_total_games < NUM_LAST_GAMES_TO_PREDICT or \
                a_total_games < NUM_LAST_GAMES_TO_PREDICT:
            prediction = WinnerPrediction.NO_DATA

        if confidence_percentage < ALLOWED_PERCENTAGE_LAST_GAMES:
            return None

        data = dict(
            prediction=prediction.value,
            confidence_percentage=format_decimal_to_n_places(
                value=Decimal(confidence_percentage)
            ),
            home_data=last_home_data,
            away_data=last_away_data
        )
        return data

    def _get_h2h_prediction(self) -> Union[Dict[str, Any], None]:
        home_wins = self.h2h['home_wins']
        away_wins = self.h2h['away_wins']
        games = self.h2h['games']
        total_h2h_games = len(games)
        if total_h2h_games < NUM_H2H_GAMES_TO_PREDICT:
            return None
        home_percentage = 100 * (home_wins / total_h2h_games)
        away_percentage = 100 * (away_wins / total_h2h_games)
        last_h_games = 0
        last_a_games = 0
        last_start_dt_game = games[0]['start_dt']
        last_games_total = 0
        last_h2h_limit = LAST_H2H_GAMES_LIMIT_PREDICTION
        for i in range(0, last_h2h_limit):
            if len(games) <= i:
                break
            game = games[i]
            h_is_winner = _is_player_winner(
                game_data=game,
                player_id=self.home_player_id
            )
            if h_is_winner:
                last_h_games += 1
            else:
                last_a_games += 1
            last_games_total += 1
        last_home_percentage = 100 * (last_h_games / last_games_total)
        last_away_percentage = 100 * (last_a_games / last_games_total)

        if last_home_percentage == last_away_percentage:
            prediction = WinnerPrediction.HOME_OR_AWAY
            confidence_percentage = 50
        elif last_home_percentage > last_away_percentage:
            prediction = WinnerPrediction.HOME_PLAYER
            confidence_percentage = last_home_percentage
        else:
            prediction = WinnerPrediction.AWAY_PLAYER
            confidence_percentage = last_away_percentage

        if confidence_percentage < ALLOWED_H2H_PERCENTAGE:
            return None

        data = dict(
            prediction=prediction.value,
            confidence_percentage=format_decimal_to_n_places(
                value=Decimal(confidence_percentage)
            ),
            home_percentage=format_decimal_to_n_places(
                value=Decimal(home_percentage)
            ),
            away_percentage=format_decimal_to_n_places(
                value=Decimal(away_percentage)
            ),
            last_game=last_start_dt_game
        )
        return data
