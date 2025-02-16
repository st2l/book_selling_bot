from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandObject
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from api.user.models import User, Refer
from bot.keyboard import main_menu

from utils import get_bot_text, identify_user
import logging

if TYPE_CHECKING:
    from aiogram.types import Message

router = Router()

# States


class StartPainState(StatesGroup):
    hello_ans = State()
    pain_text = State()
    da_ans = State()

# handlers


@router.message(Command(commands=["start"]))
async def handle_start_command(message: Message, state: FSMContext, command: CommandObject) -> None:
    if message.from_user is None:
        return

    user, is_new = await identify_user(message)

    if is_new and message.text and len(message.text.split()) > 1:
        referrer_username = command.args
        logging.info(f"Referrer username: {referrer_username}")
        try:
            referrer = await User.objects.aget(username=referrer_username)
            if referrer.id != user.id:  # Prevent self-referral
                await Refer.objects.aget_or_create(
                    refer_user=referrer,
                    invited_user=user
                )
        except User.DoesNotExist:
            pass

    if is_new:
        keyboard = ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="ПРИВЕТ")]],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await message.answer(
            text=("Привет {}!").replace('{}', message.from_user.first_name),
            reply_markup=keyboard
        )
        await state.set_state(StartPainState.hello_ans)
    else:
        try:
            await message.edit_text(
                text=await get_bot_text(name='Главное меню'),
                reply_markup=await main_menu(user)
            )
        except Exception as e:
            await message.answer(
                text=await get_bot_text(name='Главное меню'),
                reply_markup=await main_menu(user)
            )


@router.message(StartPainState.hello_ans)
async def handle_hello_ans(message: Message, state: FSMContext) -> None:
    await state.set_state(StartPainState.pain_text)
    await message.answer(
        text=(await get_bot_text(name='start_text_pain')).replace('{}', message.from_user.first_name),
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(StartPainState.pain_text)
async def handle_pain_text(message: Message, state: FSMContext) -> None:
    pain = message.text
    await state.update_data(pain=pain)
    await state.set_state(StartPainState.da_ans)

    await message.answer(
        text=(await get_bot_text(name='Выделение боли и уточняющий вопрос')).replace('{}', pain),
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
