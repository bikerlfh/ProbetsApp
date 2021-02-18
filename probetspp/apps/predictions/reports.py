from datetime import datetime, timedelta
from apps.predictions.constants import PredictionStatus
from apps.predictions import selectors
import pandas as pd


def calculate_daily_earnings(initial_amount: int):
    now = datetime.now().date()
    date_ = datetime(2021, 2, 16).date()
    data = []
    initial_amount_ = initial_amount
    while date_ <= now:
        installment = (initial_amount_ * 0.10)
        prediction_query = selectors.filter_prediction(
            start_dt=date_
        ).order_by('game__id')
        if prediction_query.exists():
            won = 0
            lost = 0
            current_amount = initial_amount_
            for item in prediction_query:
                if current_amount <= 0:
                    break
                game = item.game
                winner_id = item.player_winner_id
                odds = game.player_odds(player_id=winner_id)
                if odds is None:
                    continue
                if item.status == PredictionStatus.WON:
                    won += 1
                    current_amount += installment * (float(odds) - 1)
                    continue
                lost += 1
                current_amount -= installment * (float(odds) - 1)
            data.append(dict(
                date=date_.strftime('%Y-%m-%d'),
                initial_amount=initial_amount_,
                installment=installment,
                current_amount=current_amount,
                perdida=current_amount < initial_amount_,
                won=won,
                lost=lost
            ))
            initial_amount_ = current_amount
        date_ += timedelta(days=1)
    df = pd.DataFrame(data)
    df.to_csv('reports/predictions/test_data.csv', sep=';')
    return data
