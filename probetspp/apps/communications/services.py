from typing import Union
from asgiref.sync import async_to_sync
from apps.communications import telegram


@async_to_sync
async def send_telegram_message(
    *,
    message: str
) -> Union[None]:
    connector = telegram.TelegramConnector()
    await connector.connect()
    await connector.send_message(
        user=connector.channel_name,
        message=message
    )
