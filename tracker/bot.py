import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import CommandStart
from aiogram.types.message import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from django.conf import settings
from tracker.utils import get_deprecated_issue_assignees

bot = Bot(
    token=settings.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML")
)
dp = Dispatcher()


@dp.message(CommandStart)
async def start_message(msg: Message):
    await msg.answer(
        f"Hello {msg.from_user.mention_html()}!\n"
        f"would you like to check some issues?",
        reply_markup=issue_button(),
    )


@dp.message(F.text == "📓missed deadlines📓")
async def send_deprecated_issue_assignees(msg: Message):
    """Sends information about assignees that missed the deadline.
    :param msg: Message instance for communication with a user"""
    issues_dict = get_deprecated_issue_assignees()
    msg_str = (
        "Here is an available information "
        "about assignees that missed their draft PR deadline:"
    )

    for issue in issues_dict:
        msg_str += (
            f"\n{issue['title']} assigned to {issue['user']}"
            f"exists already {issue['days']} days "
            f"and {issue['hours']} hours"
        )

    await msg.answer(f"<blockquote>{msg_str}</blockquote>")


def issue_button():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📓missed deadlines📓")
    return builder.as_markup(resize_keyboard=True)


async def start_tg_bot():
    try:
        await dp.start_polling(bot, polling_timeout=0)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start_tg_bot())
