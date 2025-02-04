from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, Subscription, History, SubscriptionDetails, Theme, ThemePool, Notification, TaskSolved
from bot.keyboard import user_lk_keyboard, history_keyboard, back_to_main_keyboard, \
    change_theme_keyboard, notifications_settings_keyboard, view_notification_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile
from asgiref.sync import sync_to_async
import re

user_lk_router = Router()


@sync_to_async()
def get_subscription_details(subs: Subscription):
    return SubscriptionDetails.objects.get(id=subs.subscription_type.id)


@sync_to_async()
def get_history(user: User, number_of_chapter: int):
    return TaskSolved.objects.filter(user=user, task__number_of_chapter=number_of_chapter).first()


@user_lk_router.callback_query(F.data == 'user_lk')
async def user_lk_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    q = False
    subs = None
    async for el in Subscription.objects.filter(user=user):
        q = True
        subs = el
        break

    if q:
        ssss = await get_subscription_details(subs)
        status = "✔ Активна до " + (subs.date_of_creation + timedelta(days=ssss.days))\
            .strftime("%d.%m.%Y")

        progress = "\n\n<b>Прогресс:</b>\n"
        if ssss.id == 1:
            for i in range(1, 4):
                history = await get_history(user, i)
                if history:
                    progress += f"Глава {i}: ✅\n"
                else:
                    progress += f"Глава {i}: ❌\n"
        elif ssss.id == 2:
            for i in range(1, 6):
                history = await get_history
                if history:
                    progress += f"Глава {i}: ✅\n"
                else:
                    progress += f"Глава {i}: ❌\n"
        elif ssss.id == 3:
            for i in range(1, 8):
                history = await get_history(user, i)
                if history:
                    progress += f"Глава {i}: ✅\n"
                else:
                    progress += f"Глава {i}: ❌\n"
    else:
        status = "❌ Не подписан"
        progress = ""

    await call.message.edit_text(
        text=f"""<b>Личный кабинет</b>
💵 Статус подписки: {status}{progress}""",
        reply_markup=await user_lk_keyboard(user, subs),
        parse_mode='HTML'
    )

    await call.answer()


@user_lk_router.callback_query(F.data == 'purchase_history')
async def purchase_history_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='История покупок'),
        reply_markup=await history_keyboard(user)
    )


@sync_to_async()
def get_material(history: History):
    if history.methodic:
        return history.methodic
    elif history.short_methodic:
        return history.short_methodic
    elif history.book:
        return history.book


@user_lk_router.callback_query(F.data.startswith('history_'))
async def history_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    history_id = int(call.data.split('_')[1])

    history = await History.objects.aget(id=history_id)

    material = await get_material(history)
    await call.message.answer_document(
        caption=material.name,
        document=FSInputFile(material.material.path),
        reply_markup=await back_to_main_keyboard()
    )

    await call.answer()


@user_lk_router.callback_query(F.data == 'change_theme')
async def change_theme_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Изменить интересующие темы'),
        reply_markup=await change_theme_keyboard()
    )

    await call.answer()


@sync_to_async()
def change_theme(user: User, theme: ThemePool):
    Theme.objects.update(user=user, theme_type=theme)


@user_lk_router.callback_query(F.data.startswith('changetheme_'))
async def change_theme_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    theme_id = int(call.data.split('_')[1])
    theme = await ThemePool.objects.aget(id=theme_id)

    await change_theme(user, theme)

    await call.message.edit_text(
        text=await get_bot_text('Тема успешно выбрана'),
        reply_markup=await back_to_main_keyboard(),
    )

    await call.answer()


@user_lk_router.callback_query(F.data == 'notifications_settings')
async def notifications_settings_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Изменить напоминания'),
        reply_markup=await notifications_settings_keyboard(user)
    )

    await call.answer()


class NotificationStates(StatesGroup):
    text = State()
    time = State()


@user_lk_router.callback_query(F.data == 'add_notification')
async def add_notification_handler(call: CallbackQuery, state: FSMContext):
    user, is_new = await identify_user(call)

    await state.set_state(NotificationStates.text)

    await call.message.edit_text(
        text=await get_bot_text(name='Добавить текст напоминанию'),
    )

    await call.answer()


@user_lk_router.message(NotificationStates.text)
async def notification_text_handler(message: Message, state: FSMContext):
    text = message.text

    await state.update_data(text=text)
    await state.set_state(NotificationStates.time)

    await message.answer(
        text=await get_bot_text(name='Добавить время напоминания'),
    )


@user_lk_router.message(NotificationStates.time)
async def notification_time_handler(message: Message, state: FSMContext):
    user, is_new = await identify_user(message)

    time_pattern = re.compile(r'^\d{2}:\d{2}$')
    if not time_pattern.match(message.text):
        await message.answer(
            text="Неверный формат времени. Пожалуйста, используйте формат HH:MM.",
        )
        return

    hours, minutes = map(int, message.text.split(':'))
    if not (0 <= hours < 24 and 0 <= minutes < 60):
        await message.answer(
            text="Неверное время. Часы должны быть от 00 до 23, а минуты от 00 до 59.",
        )
        return

    data = await state.get_data()
    text = data['text']

    await Notification.objects.acreate(
        user=user,
        text=text,
        time=f'{hours:02}:{minutes:02}'
    )

    await message.answer(
        text=await get_bot_text(name='Напоминание добавлено'),
        reply_markup=await notifications_settings_keyboard(user)
    )

    await state.clear()


@user_lk_router.callback_query(F.data.startswith('view_notification_'))
async def view_notification_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    notification_id = int(call.data.split('_')[-1])
    notification = await Notification.objects.aget(id=notification_id)

    await call.message.edit_text(
        text=f"Текст уведомления: {notification.text}\nВремя уведомления: {notification.time}",
        reply_markup=await view_notification_keyboard(notification)
    )

    await call.answer()


class ChangeText(StatesGroup):
    id_ = State()
    text = State()


@user_lk_router.callback_query(F.data.startswith('change_text_notification_'))
async def change_text_notification_handler(call: CallbackQuery, state: FSMContext):
    user, is_new = await identify_user(call)

    notification_id = int(call.data.split('_')[-1])
    notification = await Notification.objects.aget(id=notification_id)

    await state.update_data(id_=notification_id)
    await state.set_state(ChangeText.text)

    await call.message.edit_text(
        text=await get_bot_text(name='Добавить текст напоминанию'),
    )

    await call.answer()


@sync_to_async()
def update_text_in_notification(notification_id: int, text: str):
    Notification.objects.filter(id=notification_id).update(text=text)


@user_lk_router.message(ChangeText.text)
async def change_text_notification_handler(message: Message, state: FSMContext):
    user, is_new = await identify_user(message)
    text = message.text

    await state.update_data(text=text)

    data = await state.get_data()
    text = data['text']
    notification_id = data['id_']

    await update_text_in_notification(notification_id, text)

    await message.answer(
        text=await get_bot_text(name='Текст уведомления изменен'),
        reply_markup=await notifications_settings_keyboard(user)
    )

    await state.clear()


class ChangeTime(StatesGroup):
    id_ = State()
    time = State()


@user_lk_router.callback_query(F.data.startswith('change_time_notification'))
async def change_time_notification_handler(call: CallbackQuery, state: FSMContext):
    user, is_new = await identify_user(call)

    notification_id = int(call.data.split('_')[-1])
    notification = await Notification.objects.aget(id=notification_id)

    await state.update_data(id_=notification_id)
    await state.set_state(ChangeTime.time)

    await call.message.edit_text(
        text=await get_bot_text(name='Добавить время напоминания'),
    )

    await call.answer()


@sync_to_async()
def update_time_in_notification(notification_id: int, time: str):
    Notification.objects.filter(id=notification_id).update(time=time)


@user_lk_router.message(ChangeTime.time)
async def change_time_notification_handler(message: Message, state: FSMContext):
    user, is_new = await identify_user(message)
    time = message.text

    await state.update_data(time=time)

    data = await state.get_data()
    time = data['time']
    notification_id = data['id_']

    await update_time_in_notification(notification_id, time)

    await message.answer(
        text=await get_bot_text(name='Время уведомления изменено'),
        reply_markup=await notifications_settings_keyboard(user)
    )

    await state.clear()


@sync_to_async()
def delete_notification(notification_id: int):
    Notification.objects.filter(id=notification_id).delete()


@user_lk_router.callback_query(F.data.startswith('delete_notification_'))
async def delete_notification_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)

    notification_id = int(call.data.split('_')[-1])
    await delete_notification(notification_id)

    await call.message.edit_text(
        text=await get_bot_text(name='Уведомление удалено'),
        reply_markup=await notifications_settings_keyboard(user)
    )

    await call.answer()
