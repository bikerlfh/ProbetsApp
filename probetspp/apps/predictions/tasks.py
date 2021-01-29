import logging
from datetime import datetime, timedelta

from django.utils import timezone
from apps.utils.decimal import format_decimal_to_n_places
from apps.communications import services as communications_services
from apps.flashscore import services as flash_services
from apps.games.constants import GameStatus
from apps.predictions import services


logger = logging.getLogger(__name__)


def create_periodical_prediction():
    """
    create today periodical prediction task
    """
    # update events
    flash_services.load_events()
    start_dt_from = datetime.now() + timedelta(minutes=1)
    start_dt_to = start_dt_from + timedelta(minutes=30)
    predictions = services.create_prediction_by_advance_analysis(
        status=GameStatus.SCHEDULED.value,
        start_dt_range=[
            start_dt_from,
            start_dt_to
        ]
    )
    num_predictions = len(predictions)
    for data in predictions:
        start_dt = timezone.localtime(data["start_dt"])
        confidence = format_decimal_to_n_places(value=data["confidence"])
        msg = f'{data["game"]}\n' \
              f'League: {data["league"]}\n' \
              f'Date: {start_dt.strftime("%H:%M")}\n' \
              f'Winner: {data["winner"]} (odds: {str(data["odds"])})\n' \
              f'Confidence: {confidence}'
        msg_ = msg.format(**data)
        communications_services.send_telegram_message(
            message=msg_
        )
    logger.info(
        f'create_periodical_prediction :: {num_predictions}'
    )
