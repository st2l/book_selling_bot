from __future__ import annotations

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, SubscriptionDetails, Subscription, Theme, ThemePool, Rating, SubscriptionRenewal
from bot.keyboard import go_on_subscription_keyboard, back_to_main_keyboard, \
    subscription_purchased_keyboard, rate_subscription_keyboard, theme_chosen_keyboard, subscription_renewal_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile
from asgiref.sync import sync_to_async

go_on_subscription_router = Router()


class GoOnSubscriptionStates(StatesGroup):
    subscription_type = State()


@go_on_subscription_router.callback_query(F.data == 'go_on_subscription')
async def go_on_subscription_handler(query: CallbackQuery):
    user, is_new = await identify_user(query)

    await query.message.edit_text(
        text=await get_bot_text('Текст при оформлении подписки'),
        reply_markup=await go_on_subscription_keyboard(),
    )


@go_on_subscription_router.callback_query(F.data == '1_week_subscription_purchase')
async def week_subscription_purchase_handler(query: CallbackQuery, state: FSMContext):
    user, is_new = await identify_user(query)

    subs = await SubscriptionDetails.objects.aget(id=1)

    await query.answer()
    await query.bot.send_invoice(
        chat_id=query.from_user.id,
        title=subs.name,
        description=subs.description,
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=subs.name, amount=subs.price * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )
    await state.set_state(GoOnSubscriptionStates.subscription_type)
    await state.update_data(subscription_type=subs)


@go_on_subscription_router.callback_query(F.data == '1_month_subscription_purchase')
async def week_subscription_purchase_handler(query: CallbackQuery, state: FSMContext):
    user, is_new = await identify_user(query)

    subs = await SubscriptionDetails.objects.aget(id=2)

    await query.answer()
    await query.bot.send_invoice(
        chat_id=query.from_user.id,
        title=subs.name,
        description=subs.description,
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=subs.name, amount=subs.price * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )
    await state.set_state(GoOnSubscriptionStates.subscription_type)
    await state.update_data(subscription_type=subs)


@go_on_subscription_router.callback_query(F.data == '3_month_subscription_purchase')
async def week_subscription_purchase_handler(query: CallbackQuery, state: FSMContext):
    user, is_new = await identify_user(query)

    subs = await SubscriptionDetails.objects.aget(id=3)

    await query.answer()
    await query.bot.send_invoice(
        chat_id=query.from_user.id,
        title=subs.name,
        description=subs.description,
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=subs.name, amount=subs.price * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )
    await state.set_state(GoOnSubscriptionStates.subscription_type)
    await state.update_data(subscription_type=subs)


@go_on_subscription_router.message(F.successful_payment, GoOnSubscriptionStates.subscription_type)
async def subsription_purchased(message: Message, state: FSMContext):
    user, is_new = await identify_user(message)

    data = await state.get_data()
    subs = data['subscription_type']

    await Subscription.objects.acreate(
        user=user,
        subscription_type=subs,
    )

    await message.answer(
        text=await get_bot_text('Подписка успешно оформлена'),
        reply_markup=await subscription_purchased_keyboard(),
    )
    await state.clear()


@go_on_subscription_router.callback_query(F.data.startswith('theme_'))
async def theme_chosen(call: CallbackQuery):
    user, is_new = await identify_user(call)

    theme_id = int(call.data.split('_')[1])
    theme = await ThemePool.objects.aget(id=theme_id)

    await Theme.objects.acreate(user=user, theme_type=theme)

    await call.message.edit_text(
        text=await get_bot_text('Тема успешно выбрана'),
        reply_markup=await theme_chosen_keyboard(),
    )

    await call.answer()


@go_on_subscription_router.callback_query(F.data == 'rate_subscription')
async def rate_subscription(call: CallbackQuery):
    user, is_new = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text('Оцените подписку'),
        reply_markup=await rate_subscription_keyboard(),
    )

    await call.answer()


@go_on_subscription_router.callback_query(F.data.startswith('rate_'))
async def rate_subscription(call: CallbackQuery):
    user, is_new = await identify_user(call)

    rate = int(call.data.split('_')[-1])
    await Rating.objects.acreate(user=user, rating=rate)

    await call.message.edit_text(
        text=await get_bot_text('Спасибо за оценку'),
        reply_markup=await back_to_main_keyboard(),
    )

    await call.answer()


@go_on_subscription_router.callback_query(F.data == 'renew_subscription')
async def renew_subscription_handler(call: CallbackQuery):
    user, is_new = await identify_user(call)
    
    await call.message.edit_text(
        text="Выберите тариф для продления подписки:",
        reply_markup=await subscription_renewal_keyboard()
    )

class RenewSubscriptionStates(StatesGroup):
    subscription_type = State()

@go_on_subscription_router.callback_query(F.data.startswith('renew_'))
async def process_renewal_handler(call: CallbackQuery, state: FSMContext):
    user, is_new = await identify_user(call)
    await call.answer()
    
    subscription_type = ''.join(call.data.split('_')[-1])
    logging.info(subscription_type)
    subs_id = 1 if subscription_type == '1week' else (2 if subscription_type == '1month' else 3)
    
    subs = await SubscriptionDetails.objects.aget(id=subs_id)
    
    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title=f"Продление подписки - {subs.name}",
        description=subs.description,
        payload='subscription_renewal',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[LabeledPrice(label=subs.name, amount=subs.price * 100)],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )
    
    await state.set_state(RenewSubscriptionStates.subscription_type)
    await state.update_data(subscription_type=subs)


@go_on_subscription_router.message(F.successful_payment, RenewSubscriptionStates.subscription_type)
async def renewal_purchased(message: Message, state: FSMContext):
    user, is_new = await identify_user(message)
    
    data = await state.get_data()
    subs = data['subscription_type']
    
    await SubscriptionRenewal.objects.acreate(
        user=user,
        subscription_type=subs,
    )
    
    await message.answer(
        text="Подписка успешно продлена! Она активируется автоматически после окончания текущей подписки.",
        reply_markup=await back_to_main_keyboard()
    )
    await state.clear()
