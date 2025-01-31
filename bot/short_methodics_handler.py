from __future__ import annotations

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, ShortMethodic, History
from bot.keyboard import short_methodics_keyboard, short_methodics_purchase_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile

short_methodics_router = Router()


class ShortMethodicsStates(StatesGroup):
    short_methodics_yookassa = State()


@short_methodics_router.callback_query(F.data == 'short_methodics')
async def short_methodics_handler(call: CallbackQuery):
    user = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Краткая информация для краткой методички'),
        reply_markup=await short_methodics_keyboard()
    )

    await call.answer()


@short_methodics_router.callback_query(F.data == "short_methodics_purchase")
async def short_methodics_purchase_handler(call: CallbackQuery, state: FSMContext):

    await call.answer()
    await call.message.edit_text(
        text=await get_bot_text('Оплата краткой методички'),
        reply_markup=await short_methodics_purchase_keyboard(),
    )


@short_methodics_router.callback_query(F.data == "short_methodics_yookassa")
async def short_methodics_yookassa(call: CallbackQuery, state: FSMContext):
    await call.answer()

    short_methodic = await ShortMethodic.objects.aget(id=1)
    logging.info(f"Short methodic: {short_methodic}")

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title='Краткая методичка',
        description='Покупка краткой методички',
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[LabeledPrice(label='Оплата краткой методички',
                             amount=short_methodic.price * 100)],
        need_email=True,
        send_email_to_provider=True,
    )

    await state.set_state(ShortMethodicsStates.short_methodics_yookassa)


@short_methodics_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        # всегда отвечаем утвердительно
        await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)
    except Exception as e:
        logging.error(
            f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")


@short_methodics_router.message(F.successful_payment, ShortMethodicsStates.short_methodics_yookassa)
async def short_methodics_payment_success(message: Message, state: FSMContext):
    user, _ = await identify_user(message)

    short_methodic = await ShortMethodic.objects.aget(id=1)

    await History.objects.acreate(user=user, short_methodic=short_methodic)

    logging.info(f"Short methodic material: {short_methodic.material}")
    logging.info(f"Short methodic material path: {short_methodic.material.path}")
    await message.answer_document(
        caption=await get_bot_text('Краткая методичка куплена успешно'),
        document=FSInputFile(path=short_methodic.material.path, filename='Краткая методичка')
    )

    await state.clear()
