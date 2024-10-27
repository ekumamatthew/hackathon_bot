import asyncio
import logging

from aiogram import Bot, Dispatcher
from django.conf import settings

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

dispatcher = Dispatcher()


class IssuesTrackerBot:
    def __init__(self, token):
        self.bot = Bot(token=token)

    async def send(
        self, message: str, chat_id: int = settings.TELEGRAM_CHAT_ID
    ) -> None:
        """
        Send a message.
        :param chat_id: int
        :param message: str
        """
        await self.bot.send_message(chat_id=chat_id, text=message)


BOT = IssuesTrackerBot(settings.TELEGRAM_AUTH_TOKEN)

if __name__ == "__main__":
    asyncio.run(dispatcher.start_polling(BOT.bot))
