import logging
from typing import Union
from datetime import datetime, timedelta
from apps.third_parties.flashscore import services as flash_services
from apps.third_parties.yajuego import services as yajuego_services
from apps.games.constants import GameStatus
from apps.predictions import services, communications

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
    logger.info(
        f'create_periodical_prediction :: STARTED'
    )
    logger.info(
        f'load_events :: STARTED'
    )
    flash_services.load_events()
    logger.info(
        f'load_events :: FINISHED'
    )
    logger.info(
        f'update_odds_games :: STARTED'
    )
    yajuego_services.update_odds_games()
    logger.info(
        f'update_odds_games :: FINISHED'
    )
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
    for item in predictions:
        communications.notify_prediction(
            prediction=item,
            to='me'
        )
    logger.info(f'create_periodical_prediction :: {num_predictions}')
