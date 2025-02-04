from __future__ import annotations

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, Task
from bot.keyboard import choose_tasks_keyboard, chapter_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile
from asgiref.sync import sync_to_async


tasks_router = Router()


@tasks_router.callback_query(F.data == 'tasks')
async def tasks_handler(call: CallbackQuery):
    user, _ = await identify_user(call)

    await call.message.edit_text(
        text=await get_bot_text(name='Задания'),
        reply_markup=await choose_tasks_keyboard(user)
    )

    await call.answer()


@sync_to_async()
def get_task_by_chapter(chapter: int):
    """Get task by chapter."""
    task = Task.objects.filter(number_of_chapter=chapter).first()
    return task


@tasks_router.callback_query(F.data.startswith('chapter_'))
async def chapter_handler(call: CallbackQuery):
    user, _ = await identify_user(call)

    chapter = call.data.split('_')[1]
    task = await get_task_by_chapter(chapter)

    await call.message.edit_text(
        text=task.text,
        reply_markup=await chapter_keyboard(user, task)
    )

    await call.answer()
