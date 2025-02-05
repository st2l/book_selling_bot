from datetime import datetime
from asgiref.sync import sync_to_async
from api.user.models import Notification, User
from bot.bot_instance import bot
import logging


@sync_to_async
def get_notifications_by_time(hour, minute):
    time_str = f"{hour:02d}:{minute:02d}"
    return Notification.objects.filter(time=time_str)


@sync_to_async
def get_user_from_notification(notification: Notification):
    return notification.user


async def check_and_send_notifications():
    logging.info('Checking notifications')

    now = datetime.now()
    hour, minute = now.hour, now.minute
    notifications = await get_notifications_by_time(hour, minute)

    async for notification in notifications:
        user = await get_user_from_notification(notification)
        await bot.send_message(chat_id=user.username, text=notification.text)
