from __future__ import annotations

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, Book, History
from bot.keyboard import book_keyboard, back_to_main_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile
from asgiref.sync import sync_to_async

book_router = Router()


class BookState(StatesGroup):
    purchase = State()


@book_router.callback_query(F.data == 'book')
async def book_handler(call: CallbackQuery):
    user = await identify_user(call)
    book = await Book.objects.aget(id=1)

    await call.message.edit_text(
        text=book.description,
        reply_markup=await book_keyboard()
    )

    await call.answer()


@book_router.callback_query(F.data == 'book_purchase')
async def book_purchase_handler(call: CallbackQuery, state: FSMContext):
    user = await identify_user(call)
    book = await Book.objects.aget(id=1)
    await state.set_state(BookState.purchase)

    await call.bot.send_invoice(
        chat_id=call.from_user.id,
        title=book.name,
        description=book.description,
        payload='bot_paid',
        provider_token=os.getenv('YOOKASSA_TOKEN'),
        currency='RUB',
        prices=[
            LabeledPrice(label=book.name, amount=book.price * 100)
        ],
        need_email=True,
        send_email_to_provider=True,
        start_parameter='create_invoice',
    )

    await call.answer()


@book_router.message(F.successful_payment, BookState.purchase)
async def book_payment_handler(message: Message, state: FSMContext):
    user, _ = await identify_user(message)
    book = await Book.objects.aget(id=1)
    await state.clear()

    history = await History.objects.acreate(user=user, book=book)

    await message.answer_document(
        caption=await get_bot_text(name='Успешная покупка книги'),
        document=FSInputFile(book.material.path),
        reply_markup=await back_to_main_keyboard()
    )
