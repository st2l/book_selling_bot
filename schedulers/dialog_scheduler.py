from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from api.user.models import Subscription, DialogTask, DialogResponse
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot_instance import bot
import logging
import pytz

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
        [InlineKeyboardButton(text="Дать ответ", callback_data=f"dialog_answer_{task.id}")]
    ])

    await bot.send_message(
        chat_id=user.username,
        text=task.message,
        reply_markup=keyboard
    )

@sync_to_async
def get_user_from_subscription(subscription: Subscription):
    return subscription.user

async def check_and_send_dialogs():
    now = datetime.now(pytz.utc)
    current_hour = now.hour
    
    # Определяем время дня TODO: change for production
    time_of_day = "утро" if current_hour == 10 else "вечер"
    
    logging.info(f'Checking dialogs for {time_of_day}')
    
    subscriptions = await get_active_subscriptions()
    
    async for subscription in subscriptions:
        days_active = (now - subscription.date_of_creation).days + 1
        
        if days_active <= 90:  # Максимальное количество дней
            dialog_task = await get_dialog_task(days_active, time_of_day)
            
            if dialog_task:
                user = await get_user_from_subscription(subscription)
                await send_dialog_task(user, dialog_task)