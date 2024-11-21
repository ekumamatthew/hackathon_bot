from asgiref.sync import async_to_sync

from celery import shared_task
from .models import CustomUser, TelegramUser
from .utils import get_user_revisions
from .telegram.bot import send_revision_messages

@shared_task
def fetch_approvals(tele_id: str):
    try:
        tel_user = TelegramUser.objects.get(
            telegram_id = tele_id
        )
    except TelegramUser.DoesNotExist:
        return
    
    reviews = get_user_revisions(str(tel_user.id))
    if reviews:
        async_to_sync(send_revision_messages)(tel_user.id, reviews)
    