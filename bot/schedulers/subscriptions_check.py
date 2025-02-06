from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from api.user.models import Subscription, SubscriptionDetails, User, Notification, Theme, DialogResponse
from bot.bot_instance import bot
import logging
import pytz
import os
from aiogram.types import FSInputFile


@sync_to_async
def get_active_subscriptions():
    return Subscription.objects.all()


@sync_to_async
def delete_subscription(subscription: Subscription):
    user = subscription.user
    subscription.delete()
    Notification.objects.filter(user=user).delete()
    Theme.objects.filter(user=user).delete()


@sync_to_async
def get_user_from_subscription(subscription: Subscription):
    return subscription.user


@sync_to_async
def get_subscription_details(subscription: Subscription):
    return subscription.subscription_type


@sync_to_async
def get_user_dialog_responses(user: User):
    return DialogResponse.objects.filter(user=user).order_by('dialog_task__day_number', 'created_at')


@sync_to_async
def format_dialog_responses(responses):
    formatted_text = "Ваши ответы на диалоги:\n\n"
    for response in responses:
        formatted_text += f"День {response.dialog_task.day_number} ({response.dialog_task.time_of_day}):\n"
        formatted_text += f"Задание: {response.dialog_task.message}\n"
        formatted_text += f"Ваш ответ: {response.response_text}\n"
        formatted_text += f"Дата ответа: {response.created_at.strftime('%d.%m.%Y %H:%M')}\n\n"
    return formatted_text


@sync_to_async
def save_responses_to_file(text: str, username: str):
    filename = f"responses_{username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = f"media/responses/{filename}"
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(text)
    return filepath


async def check_and_notify_subscriptions():
    logging.info('Checking subscriptions')

    now = datetime.now(pytz.utc)
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
            # Get and format dialog responses
            responses = await get_user_dialog_responses(user)
            formatted_text = await format_dialog_responses(responses)
            filepath = await save_responses_to_file(formatted_text, user.username)
            
            # Send end subscription message and responses file
            await bot.send_message(chat_id=user.username, text="Ваша подписка закончилась.")
            await bot.send_document(
                chat_id=user.username,
                document=FSInputFile(filepath),
                caption="Ваши ответы на диалоги за время подписки"
            )
            
            # Delete subscription and cleanup
            await delete_subscription(subscription)
            
            # Clean up the temporary file
            os.remove(filepath)
