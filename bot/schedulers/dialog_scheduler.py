from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from api.user.models import Subscription, DialogTask, DialogResponse, User
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot_instance import bot
import pytz
from pytz import timezone
from django.db.models import Q
import logging


@sync_to_async
def get_active_subscriptions():
    return Subscription.objects.all()


@sync_to_async
def get_dialog_task(day_number: int, time_of_day: str):
    return DialogTask.objects.filter(
        day_number=day_number,
        time_of_day=time_of_day
    ).first()


async def send_dialog_task(user, task):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Записать ответ", callback_data=f"dialog_answer_{task.id}")]
    ])

    await bot.send_message(
        chat_id=user.username,
        text=task.message,
        reply_markup=keyboard
    )


@sync_to_async
def get_user_from_subscription(subscription: Subscription):
    return subscription.user


@sync_to_async
def get_subscription(user: User):
    return Subscription.objects.filter(user=user).first()


async def send_dialog_to_user(user):
    current_time = datetime.now(timezone('Europe/Moscow')).strftime('%H:%M')
    if current_time == user.morning_dialog_time:
        time_of_day = 'утро'
    else:
        time_of_day = 'вечер'

    sub = await get_subscription(user)
    now = datetime.now(timezone('Europe/Moscow'))
    days_passed = (now - sub.date_of_creation).days + 1
    logging.info(f"Days passed: {days_passed}")

    task = await get_dialog_task(days_passed, time_of_day)
    if task:
        await send_dialog_task(user, task)


async def check_and_send_dialogs():
    now = datetime.now(timezone('Europe/Moscow'))
    current_time = now.strftime('%H:%M')
    logging.info(f"Current time: {current_time}")

    async for user in User.objects.filter(
        Q(morning_dialog_time=current_time) |
        Q(evening_dialog_time=current_time)
    ):
        subs = await get_subscription(user)
        if subs:
            await send_dialog_to_user(user)
