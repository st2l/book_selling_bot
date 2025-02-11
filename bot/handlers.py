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
    from aiogram.types import Message

router = Router()

# States


class StartPainState(StatesGroup):
    pain_text = State()
    da_ans = State()

# handlers


@router.message(Command(commands=["start"]))
async def handle_start_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    user, is_new = await identify_user(message)

    # TODO: ADD usage of is_new variable
    await message.answer(text=(await get_bot_text(name='start_text_pain')).replace('{}', message.from_user.first_name))
    await state.set_state(StartPainState.pain_text)


@router.message(StartPainState.pain_text)
async def handle_pain_text(message: Message, state: FSMContext) -> None:
    pain = message.text
    await state.update_data(pain=pain)
    await state.set_state(StartPainState.da_ans)

    await message.answer(
        text=(await get_bot_text(name='Выделение боли и уточняющий вопрос')).replace('{}', pain)
    )


@router.message(StartPainState.da_ans)
async def handle_da_ans(message: Message, state: FSMContext) -> None:
    ans = message.text
    user, is_new = await identify_user(message)
    await state.clear()

    await message.answer(
        text=(await get_bot_text(name='Стартовое сообщение и рекомендацию по использованию подписки')),
        reply_markup=await main_menu(user=user),
    )
