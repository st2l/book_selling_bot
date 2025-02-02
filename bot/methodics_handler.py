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
    back_to_main_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile

methodics_router = Router()


class MethodicsStates(StatesGroup):
    methodics_yookassa = State()


@methodics_router.callback_query(F.data == 'methodics')
async def methodics_handler(call: CallbackQuery):
    user = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Информация для методичек'),
        reply_markup=await choose_three_methodics_keyboard()
    )

    await call.answer()


@methodics_router.callback_query(F.data == 'methodic_1')
async def methodic_1_handler(call: CallbackQuery):
    user = await identify_user(call)

    methodic = await Methodic.objects.aget(id=1)

    await call.message.edit_text(
        text=methodic.description,
        reply_markup=await methodic_1_keyboard()
    )

    await call.answer()


@methodics_router.callback_query(F.data == "methodic_1_purchase")
async def methodic_1_purchase(call: CallbackQuery, state: FSMContext):

    await call.answer()

    methodic = await Methodic.objects.aget(name='Методичка 1')
    logging.info(f"Methodic: {methodic}")

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title=methodic.name,
        description='Покупка методички №1',
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=methodic.name, amount=methodic.price * 100)
        ],
        start_parameter='create_invoice',
    )

    await state.set_state(MethodicsStates.methodics_yookassa)
    await state.update_data(methodic_name=methodic.name)


@methodics_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@methodics_router.message(F.successful_payment, MethodicsStates.methodics_yookassa)
async def process_successful_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    methodic_name = data.get('methodic_name')

    user, _ = await identify_user(message)
    methodic = await Methodic.objects.aget(name=methodic_name)

    await History.objects.acreate(
        user=user,
        methodic=methodic,
    )

    await message.answer_document(
        caption=await get_bot_text("Методичка куплена успешно"),
        document=FSInputFile(methodic.material.path),
        reply_markup=await back_to_main_keyboard()
    )
    await state.clear()
