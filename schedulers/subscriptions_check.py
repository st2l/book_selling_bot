from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from api.user.models import Subscription, SubscriptionDetails, User
from bot.bot_instance import bot
import logging
import pytz


@sync_to_async
def get_active_subscriptions():
    return Subscription.objects.all()


@sync_to_async
def delete_subscription(subscription: Subscription):
    subscription.delete()


@sync_to_async
def get_user_from_subscription(subscription: Subscription):
    return subscription.user


@sync_to_async
def get_subscription_details(subscription: Subscription):
    return subscription.subscription_type


async def check_and_notify_subscriptions():
    logging.info('Checking subscriptions')

    now = datetime.now(pytz.utc)  # Make 'now' timezone-aware
    subscriptions = await get_active_subscriptions()

    async for subscription in subscriptions:
        user = await get_user_from_subscription(subscription)
        subscription_details = await get_subscription_details(subscription)
        subscription_end_date = subscription.date_of_creation + \
            timedelta(days=subscription_details.days)
        days_left = (subscription_end_date - now).days

        logging.info(f"User {user.username} has {days_left} days left")

        if days_left == 2:
            await bot.send_message(chat_id=user.username, text="Ваша подписка заканчивается через 2 дня.")
        elif days_left <= 0:
            await bot.send_message(chat_id=user.username, text="Ваша подписка закончилась.")
            await delete_subscription(subscription)
