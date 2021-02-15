import logging
from typing import Optional, Union
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from apps.utils.decimal import format_decimal_to_n_places
from apps.telegram_bot.typing import Message
from apps.telegram_bot.constants import Emoji, TELEGRAM_CHANNEL_NAME
from apps.telegram_bot import services as telegram_services
from apps.predictions.constants import PredictionStatus
from apps.predictions import selectors

logger = logging.getLogger(__name__)


def notify_prediction(
    *,
    prediction_id: int,
    to: Optional[str] = TELEGRAM_CHANNEL_NAME
) -> Union[None]:
    prediction_qry = selectors.filter_prediction_by_id(
        prediction_id=prediction_id
    )
    if not prediction_qry.exists():
        msg = f'{prediction_id} does not exists'
        logger.warning(f'notify_prediction :: {msg}')
        raise ValidationError(msg)
    prediction = prediction_qry.first()
    status = PredictionStatus(prediction.status)
    if status != PredictionStatus.DEFAULT:
        msg = 'prediction status does not allowed'
        logger.warning(f'notify_prediction :: {msg}')
        raise ValidationError(msg)
    game = prediction.game
    league = str(game.league)
    start_dt = timezone.localtime(game.start_dt).strftime("%H:%M")
    confidence = format_decimal_to_n_places(value=prediction.confidence)
    odds = game.player_odds(player_id=prediction.player_winner_id)
    if odds:
        odds = f'({Emoji.DOLLAR.value} {odds})'
    else:
        odds = ''
    winner = str(prediction.player_winner)
    msg = f'<b>{Emoji.FIRE.value} {str(game)} {Emoji.FIRE.value}</b>\n' \
          f'{Emoji.TROPHY.value} {league} - ' \
          f'{Emoji.WATCH.value} {start_dt}\n' \
          f'<b>{Emoji.PING_PONG.value} {winner} {odds}</b>\n' \
          f'{Emoji.CHECK_BUTTON.value} {confidence}%\n\n' \
          f'{Emoji.ONLY_ADULTS.value} Juega con responsabilidad'
    message = Message(
        message=msg,
        user=to
    )
    telegram_services.send_telegram_messages(
        messages=[message]
    )
