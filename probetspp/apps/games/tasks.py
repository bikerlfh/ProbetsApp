import logging
from typing import Union
from datetime import datetime, timedelta
from apps.third_parties.flashscore import services as flash_services
from apps.games.constants import GameStatus
from apps.games import selectors, services

logger = logging.getLogger(__name__)


def update_old_scheduled_games() -> Union[None]:
    yesterday = datetime.now() - timedelta(days=1)
    game_qry = selectors.filter_games(
        status=[
            GameStatus.SCHEDULED.value,
            GameStatus.IN_LIVE.value,
        ]
    ).filter(
        start_dt__date__lte=yesterday.date(),
    ).order_by('start_dt')
    for game in game_qry:
        data = flash_services.get_event_detail(
            external_id=game.external_id
        )
        if not data:
            logger.error(
                f'update_old_games :: no data :: '
                f'game {game.id} ({game.external_id})'
            )
            continue

        if 'error' in data:
            logger.warning(
                f'update_old_games :: error in data game {game.id}'
            )
            game.status = GameStatus.NO_DATA.value
            game.save()
            continue
        status = data['status']
        h_score = data['home_score']
        a_score = data['away_score']
        l_score = data['line_score']
        game.status = status
        status_ = [
            GameStatus.DEFAULT.value,
            GameStatus.SCHEDULED.value,
            GameStatus.IN_LIVE.value
        ]
        if status in status_:
            logger.warning(
                f'update_old_games :: '
                f'game {game.id} not finished'
            )
        if status == GameStatus.FINISHED.value and not l_score:
            logger.error(
                f'update_old_games :: game {game.id} '
                f'finished without line score'
            )
            continue
        data = dict(
            game=game,
            status=status,
            home_score=h_score,
            away_score=a_score,
            line_score=l_score
        )
        services.update_game(**data)
        logger.info(
            f'update_old_games :: game {game.id} updated'
        )
