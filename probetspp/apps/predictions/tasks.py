import logging
from typing import Union
from datetime import datetime, timedelta
from django.utils import timezone
from apps.utils.decimal import format_decimal_to_n_places
from apps.communications.typing import Message
from apps.communications import services as communications_services
from apps.third_parties.flashscore import services as flash_services
from apps.third_parties.yajuego import services as yajuego_services
from apps.games.constants import GameStatus
from apps.predictions import services


logger = logging.getLogger(__name__)


def update_events_data() -> Union[None]:
    try:
        flash_services.load_events()
    except Exception as exc:
        logger.exception(
            f'update_events_data :: {exc}'
        )


def create_periodical_prediction() -> Union[None]:
    """
    create today periodical prediction task
    """
    start_dt_from = datetime.now()
    yajuego_services.update_odds_games()
    start_dt_to = start_dt_from + timedelta(minutes=30)
    predictions = services.create_prediction_by_advance_analysis(
        status=GameStatus.SCHEDULED.value,
        start_dt_range=[
            start_dt_from,
            start_dt_to
        ]
    )
    num_predictions = len(predictions)
    messages = []
    for data in predictions:
        start_dt = timezone.localtime(data["start_dt"])
        confidence = format_decimal_to_n_places(value=data["confidence"])
        odds = data["odds"]
        winner = f'{data["winner"]}'
        if odds:
            winner = f'{data["winner"]} (odds: {str(data["odds"])})'
        msg = f'{data["game"]}\n' \
              f'League: {data["league"]}\n' \
              f'Date: {start_dt.strftime("%H:%M")}\n' \
              f'Winner: {winner}\n' \
              f'Confidence: {confidence}'
        message = Message(
            message=msg.format(**data),
            user='me'
        )
        messages.append(message)
    communications_services.send_telegram_messages(
        messages=messages
    )
    logger.info(
        f'create_periodical_prediction :: {num_predictions}'
    )
