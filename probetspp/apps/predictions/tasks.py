import logging
from datetime import datetime, timedelta

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
    start_dt_from = datetime.now()
    start_dt_to = start_dt_from + timedelta(minutes=30)
    predictions = services.create_prediction_by_advance_analysis(
        status=GameStatus.SCHEDULED.value,
        start_dt_range=[
            start_dt_from,
            start_dt_to
        ]
    )
    num_predictions = len(predictions)
    msg = 'Game: {game}\n' \
          'League: {league}\n' \
          'Start_dt:{start_dt.strftime("%Y-%m-%d %H:%M:%s")}\n' \
          'Winner: {winner}\n' \
          'Confidence: {confidence}'
    for data in predictions:
        msg_ = msg.format(**data)
        communications_services.send_telegram_message(
            message=msg_
        )
    logger.info(
        f'create_periodical_prediction :: {num_predictions}'
    )
