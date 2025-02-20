from __future__ import annotations

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, Methodic, History, Rating
from bot.keyboard import choose_three_methodics_keyboard, methodic_1_keyboard, \
    back_to_main_keyboard, methodic_2_keyboard, methodic_3_keyboard, methodic_all_keyboard
from bot.check_and_process_referal import check_and_process_referral

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async

methodics_router = Router()


class MethodicsStates(StatesGroup):
    methodics_yookassa = State()
    rating = State()


@methodics_router.callback_query(F.data == 'methodics')
async def methodics_handler(call: CallbackQuery):
    user = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Информация для методичек'),
        reply_markup=await choose_three_methodics_keyboard()
    )

    await call.answer()

# ########################################################
# #### Methodic 1 ########################################
# ########################################################


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
    methodic = await Methodic.objects.aget(id=1)
    logging.info(f"Methodic: {methodic}")

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title=methodic.name,
        description=methodic.purchase_description or methodic.description,  # Используем purchase_description если есть
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=methodic.name, amount=methodic.price * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )

    await state.set_state(MethodicsStates.methodics_yookassa)
    await state.update_data(methodic_id=methodic.id)


@methodics_router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@methodics_router.message(F.successful_payment, MethodicsStates.methodics_yookassa)
async def process_successful_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    methodic_id = data.get('methodic_id')
    user, _ = await identify_user(message)

    await check_and_process_referral(user)

    from api.user.models import RatingRequest
    from datetime import datetime, timedelta
    await RatingRequest.objects.acreate(
        user=user,
        methodic=methodic,
        date_to_send=datetime.now() + timedelta(days=7)
    )

    # if ALL methodics
    if methodic_id == "Все методички":
        methodics = await sync_to_async(Methodic.objects.all, thread_sensitive=True)()
        async for methodic in methodics:
            user, _ = await identify_user(message)
            await History.objects.acreate(
                user=user,
                methodic=methodic,
            )

            await message.answer_document(
                caption=await get_bot_text("Методичка куплена успешно"),
                document=FSInputFile(methodic.material.path)
            )
            
    else:
        user, _ = await identify_user(message)
        methodic = await Methodic.objects.aget(id=methodic_id)

        await History.objects.acreate(
            user=user,
            methodic=methodic,
        )

        await message.answer_document(
            caption=await get_bot_text("Методичка куплена успешно"),
            document=FSInputFile(methodic.material.path)
        )
        
    # Запрос оценки
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐" * i, callback_data=f"rate_{methodic.id}_{i}")] for i in range(5, 0, -1)
    ])
    
    await message.bot.send_message(
        chat_id=user.id,
        text="Пожалуйста, оцените сервис от 1 до 5 звезд:",
        reply_markup=keyboard
    )
    
    await state.set_state(MethodicsStates.rating)


@sync_to_async
def save_methodic_rating(user: User, rating: int):
    Rating.objects.create(user=user, rating=rating)




# ########################################################
# #### Methodic 2 ########################################
# ########################################################
@methodics_router.callback_query(F.data == 'methodic_2')
async def methodic_1_handler(call: CallbackQuery):
    user = await identify_user(call)

    methodic = await Methodic.objects.aget(id=2)

    await call.message.edit_text(
        text=methodic.description,
        reply_markup=await methodic_2_keyboard()
    )

    await call.answer()


@methodics_router.callback_query(F.data == "methodic_2_purchase")
async def methodic_2_purchase(call: CallbackQuery, state: FSMContext):
    await call.answer()
    methodic = await Methodic.objects.aget(id=2)
    logging.info(f"Methodic: {methodic}")

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title=methodic.name,
        description=methodic.purchase_description or methodic.description,  # Используем purchase_description если есть
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=methodic.name, amount=methodic.price * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )

    await state.set_state(MethodicsStates.methodics_yookassa)
    await state.update_data(methodic_id=methodic.id)


# ########################################################
# #### Methodic 3 ########################################
# ########################################################
@methodics_router.callback_query(F.data == 'methodic_3')
async def methodic_3_handler(call: CallbackQuery):
    user = await identify_user(call)

    methodic = await Methodic.objects.aget(id=3)

    await call.message.edit_text(
        text=methodic.description,
        reply_markup=await methodic_3_keyboard()
    )

    await call.answer()


@methodics_router.callback_query(F.data == "methodic_3_purchase")
async def methodic_1_purchase(call: CallbackQuery, state: FSMContext):
    await call.answer()
    methodic = await Methodic.objects.aget(id=3)
    logging.info(f"Methodic: {methodic}")

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title=methodic.name,
        description=methodic.purchase_description or methodic.description,  # Используем purchase_description если есть
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=methodic.name, amount=methodic.price * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )

    await state.set_state(MethodicsStates.methodics_yookassa)
    await state.update_data(methodic_id=methodic.id)


# ########################################################
# #### Methodic all ########################################
# ########################################################
@methodics_router.callback_query(F.data == 'methodic_all')
async def methodic_3_handler(call: CallbackQuery):
    user = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text('Описание при покупке всех методичек'),
        reply_markup=await methodic_all_keyboard()
    )

    await call.answer()


@methodics_router.callback_query(F.data == "methodic_all_purchase")
async def methodic_1_purchase(call: CallbackQuery, state: FSMContext):

    await call.answer()

    methodics = await sync_to_async(Methodic.objects.all, thread_sensitive=True)()
    summa = 0

    async for methodic in methodics:
        summa += methodic.price

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title="Все методички",
        description='Покупка всех трех методичек',
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label="Все методички", amount=summa * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )

    await state.set_state(MethodicsStates.methodics_yookassa)
    await state.update_data(methodic_id="Все методички")
