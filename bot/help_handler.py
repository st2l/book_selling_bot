from __future__ import annotations

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, Methodic, History
from bot.keyboard import choose_three_methodics_keyboard, methodic_1_keyboard, \
    back_to_main_keyboard, methodic_2_keyboard, methodic_3_keyboard, methodic_all_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from asgiref.sync import sync_to_async

help_router = Router()


@help_router.callback_query(F.data == 'help')
async def help_handler(call: CallbackQuery):
    user, _ = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Помощь'),
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='FAQ', callback_data='faq')],
                [InlineKeyboardButton(text='◀️ Назад', callback_data='main_menu')]
            ]
        )
    )

    await call.answer()
