from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User
from bot.keyboard import main_menu

from utils import get_bot_text, identify_user

if TYPE_CHECKING:
    from aiogram.types import Message, CallbackQuery

main_menu_router = Router()


@main_menu_router.callback_query(F.data == 'main_menu')
async def main_menu_handler(call: CallbackQuery):
    user = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Главное меню'),
        reply_markup=await main_menu(user)
    )

    await call.answer()
