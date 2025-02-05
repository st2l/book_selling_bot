from datetime import datetime
from asgiref.sync import sync_to_async
from celery import shared_task
from api.user.models import Notification, User
from bot.bot_instance import bot
import logging


@sync_to_async
def get_notifications_by_time(hour, minute):
    return Notification.objects.filter(time__hour=hour, time__minute=minute)


@sync_to_async
def get_user_by_id(user_id):
    return User.objects.get(id=user_id)


@shared_task
async def check_and_send_notifications():
    logging.info('Checking notifications')

    now = datetime.now()
    hour, minute = now.hour, now.minute
    notifications = await get_notifications_by_time(hour, minute)

    for notification in notifications:
        user = await get_user_by_id(notification.user_id)
        await bot.send_message(chat_id=user.id, text=notification.text)
