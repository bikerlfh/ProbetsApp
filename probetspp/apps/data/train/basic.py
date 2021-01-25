"""
Train to results of a day and predictions created
"""
from datetime import date, datetime
from django.db.models import F
import pandas as pd

from apps.predictions.constants import PredictionStatus
from apps.predictions import selectors as pdt_selectors
from apps.data import selectors

date_ = datetime.strptime('2021-01-22', '%Y-%m-%d')


class BasicTrain:
    def __init__(
        self,
        start_dt: date = date_
    ):
        self.start_dt = start_dt
        self.predictions = pdt_selectors.filter_prediction(
            start_dt=start_dt,
            status=[
                PredictionStatus.WON.value,
                PredictionStatus.LOSE.value
            ]
        ).annotate(
            h_id=F('game__home_player_id'),
            a_id=F('game__away_player_id')
        ).values(
            'id', 'game_id', 'h_id', 'a_id', 'status',
            'player_winner', 'confidence'
        )
        self.t_pdt = len(self.predictions)
        df = pd.DataFrame(self.predictions)
        self.df = df
        self.wg_df = df[df['status'] == PredictionStatus.WON.value]
        self.lg_df = df[df['status'] == PredictionStatus.LOSE.value]
        self.n_wg = len(self.wg_df)
        self.n_lg = len(self.lg_df)
        self.init_w_per = (self.n_wg / self.t_pdt) * 100
        self.init_l_per = (self.n_lg / self.t_pdt) * 100
        self._load_default_wt()
        print(f'Total pdt:{self.t_pdt}')
        print(f'Won Games:{self.n_wg}')
        print(f'Lost games:{self.n_lg}')
        print(f'Won %:{self.init_w_per}')
        print(f'Lost %:{self.init_l_per}')

    def _load_default_wt(self):
        d_ = selectors.filter_default_data_weights().first()
        wt_h2h = d_['wt_h2h']
        wt_last_games = d_['wt_last_games']
        wt_d_opp = d_['wt_direct_opponents']
        wt_player = d_['wt_games'] + d_['wt_sets'] + d_['wt_points']
        wt_player += d_['wt_games_sold'] + d_['wt_predictions']
        wt_player = wt_player / 5
        wt_total = wt_h2h + wt_last_games
        wt_total += wt_d_opp + wt_player
        self.default_wt = dict(
            wt_h2h=d_['wt_h2h'],
            wt_lg=d_['wt_last_games'],
            wt_player=wt_player,
            wt_d_opp=d_['wt_direct_opponents'],
            wt_total=wt_total
        )

    def analyse_games(self):
        lg_data = self.lg_df.to_dict(orient='records')
        for game in lg_data:
            pass
