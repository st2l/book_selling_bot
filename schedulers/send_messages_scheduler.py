from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from asgiref.sync import sync_to_async
from api.user.models import SendMessage, User, Theme, Subscription
from bot.bot_instance import bot
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.media_group import MediaGroupBuilder
import logging
import pytz
import asyncio


@sync_to_async
def get_messages_to_send():
    now = datetime.now(pytz.utc)
    return SendMessage.objects.filter(date_to_send__lte=now)


@sync_to_async
def mark_message_as_sent(message: SendMessage):
    message.delete()


@sync_to_async
def get_users_by_theme(message: SendMessage):
    theme = message.theme_type
    return User.objects.filter(theme__theme_type=theme)


@sync_to_async
def get_all_users():
    ans = []
    for el in User.objects.all():
        subs = Subscription.objects.filter(user=el)
        if subs:
            ans.append(el)
    return ans


async def send_message_to_users(message: SendMessage, users):
    media_group = MediaGroupBuilder()
    if message.photo_1:
        media_group.add_photo(media=FSInputFile(message.photo_1.path))
    if message.photo_2:
        media_group.add_photo(media=FSInputFile(message.photo_2.path))
    if message.photo_3:
        media_group.add_photo(media=FSInputFile(message.photo_3.path))
    if message.photo_4:
        media_group.add_photo(media=FSInputFile(message.photo_4.path))
    if message.photo_5:
        media_group.add_photo(media=FSInputFile(message.photo_5.path))
    if message.video_1:
        media_group.add_video(media=FSInputFile(message.video_1.path))
    if message.video_2:
        media_group.add_video(media=FSInputFile(message.video_2.path))
    if message.video_3:
        media_group.add_video(media=FSInputFile(message.video_3.path))

    kb = None
    if message.button_text != 'option1':
        arr = []
        if message.button_text == 'option2':
            arr.append([InlineKeyboardButton(
                text='Перейти в ЛК', callback_data='user_lk')])
        if message.button_text == 'option3':
            arr.append([InlineKeyboardButton(
                text='Перейти к заданиям', callback_data='tasks')])
        if message.button_text == 'option4':
            arr.append([InlineKeyboardButton(
                text='Купить книгу', callback_data='book')])
        if message.button_text == 'option5':
            arr.append([InlineKeyboardButton(
                text='Купить методички', callback_data='methodic')])
        kb = InlineKeyboardMarkup(inline_keyboard=arr)

    sent = set()
    for user in users:
        logging.info(f'Sending message to {user.username}')
        if user in sent:
            continue
        try:
            if message.photo_1 or message.photo_2 or message.photo_3 or message.photo_4 or message.photo_5 or message.video_1 or message.video_2 or message.video_3:
                if kb is None:
                    media_group.caption = message.message
                    await bot.send_media_group(chat_id=user.username, media=media_group.build())
                else:
                    await bot.send_media_group(chat_id=user.username, media=media_group.build())
                    await bot.send_message(chat_id=user.username, text=message.message, reply_markup=kb)
            else:
                await bot.send_message(chat_id=user.username, text=message.message, reply_markup=kb)
        except Exception as e:
            logging.error(f'Error sending message to {user.username}: {e}')
        sent.add(user)


async def check_and_send_messages():
    await asyncio.sleep(5)
    logging.info('Checking messages to send')

    messages = await get_messages_to_send()

    async for message in messages:
        if message.theme_all:
            users = await get_all_users()
        else:
            users = await get_users_by_theme(message)

        await send_message_to_users(message, users)
        await mark_message_as_sent(message)
