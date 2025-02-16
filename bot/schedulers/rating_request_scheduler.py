from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from api.user.models import RatingRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from bot.bot_instance import bot
import logging
import pytz

@sync_to_async
def get_rating_requests():
    now = datetime.now(pytz.utc)
    return RatingRequest.objects.filter(date_to_send__lte=now)

@sync_to_async
def delete_rating_request(request: RatingRequest):
    request.delete()

async def check_and_send_rating_requests():
    logging.info('Checking rating requests')
    
    requests = await get_rating_requests()
    
    async for request in requests:
        try:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⭐" * i, callback_data=f"rate_{i}")] for i in range(5, 0, -1)
            ])
            
            product_type = "методичку" if request.methodic else ("краткую методичку" if request.short_methodic else "книгу")
            
            await bot.send_message(
                chat_id=request.user.username,
                text=f"Пожалуйста, оцените {product_type}, которую вы приобрели неделю назад:",
                reply_markup=keyboard
            )
            
            await delete_rating_request(request)
            
        except Exception as e:
            logging.error(f"Error sending rating request to {request.user.username}: {e}") 