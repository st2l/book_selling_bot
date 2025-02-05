from __future__ import annotations
from deepseek import deepseek

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, Task, TaskSolved
from bot.keyboard import choose_tasks_keyboard, chapter_keyboard, back_to_main_keyboard

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


@sync_to_async()
def get_task_by_id(task_id: int):
    """Get task by id."""
    task = Task.objects.filter(id=task_id).first()
    return task


@sync_to_async()
def add_solved_task(user: User, task: Task, text: str):
    """Add solved task."""
    TaskSolved.objects.create(user=user, task=task, text=text)


class CompleteTaskStates(StatesGroup):
    task_id = State()
    text = State()


@tasks_router.callback_query(F.data.startswith('complete_task_'))
async def completed_task_handler(call: CallbackQuery, state: FSMContext):
    user, _ = await identify_user(call)

    task_id = call.data.split('_')[2]
    await state.set_state(CompleteTaskStates.text)
    await state.update_data(task_id=task_id)

    await call.message.edit_text(
        text=await get_bot_text(name='Введите решение задачи'),
        reply_markup=await back_to_main_keyboard()
    )

    await call.answer()


@tasks_router.message(CompleteTaskStates.text)
async def completed_task_text_handler(message: Message, state: FSMContext):
    user, _ = await identify_user(message)

    data = await state.get_data()
    task_id = data.get('task_id')
    task = await get_task_by_id(task_id)

    await add_solved_task(user, task, text=message.text)
    await message.answer(
        text=await get_bot_text(name='Задача решена успешно'),
        reply_markup=await back_to_main_keyboard()
    )
    await state.clear()


@sync_to_async()
def get_solved_task_text(user: User, task: Task):
    """Get solved task text."""
    task_solved = TaskSolved.objects.filter(user=user, task=task).first()
    return task_solved.text


@tasks_router.callback_query(F.data.startswith('view_answer_'))
async def view_asnwer_handler(call: CallbackQuery):
    user, _ = await identify_user(call)

    task_id = call.data.split('_')[2]
    task = await get_task_by_id(task_id)

    task_solved_text = await get_solved_task_text(user, task)

    await call.message.edit_text(
        text=task_solved_text,
        reply_markup=await chapter_keyboard(user, task)
    )

    await call.answer()


class DiscussTaskStates(StatesGroup):
    task_id = State()
    text = State()


@tasks_router.callback_query(F.data.startswith('discuss_'))
async def discuss_handler(call: CallbackQuery, state: FSMContext):
    user, _ = await identify_user(call)

    await state.set_state(DiscussTaskStates.text)
    await state.set_state(task_id=call.data.split('_')[1])

    task_id = call.data.split('_')[1]
    task = await get_task_by_id(task_id)

    await call.message.edit_text(
        text=await get_bot_text(name='Обсуждение главы'),
        reply_markup=await chapter_keyboard(user, task)
    )

    await call.answer()


@tasks_router.message(DiscussTaskStates.text)
async def discuss_text_handler(message: Message, state: FSMContext):
    user, _ = await identify_user(message)

    data = await state.get_data()
    task_id = data.get('task_id')
    task = await get_task_by_id(task_id)

    # Получаем ответ от DeepSeek
    user_question = message.text
    deepseek_response = deepseek.ask_question_in_chapter(user_question)

    # Отправляем ответ пользователю
    await message.answer(deepseek_response)

    await state.clear()
