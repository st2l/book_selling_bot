from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User
from bot.keyboard import short_methodics_keyboard

from utils import get_bot_text, identify_user

if TYPE_CHECKING:
    from aiogram.types import Message, CallbackQuery

short_methodics_router = Router()


@short_methodics_router.callback_query(F.data == 'short_methodics')
async def short_methodics_handler(call: CallbackQuery):
    user = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Краткая информация для краткой методички'),
        reply_markup=await short_methodics_keyboard()
    )

    await call.answer()
