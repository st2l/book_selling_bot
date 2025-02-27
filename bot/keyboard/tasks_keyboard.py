from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.user.models import User, Task, Subscription, TaskSolved
from asgiref.sync import sync_to_async


@sync_to_async()
def get_subscryption_type_id(user: User):
    """Get user subscryption type id."""
    subs: Subscription = Subscription.objects.filter(user=user).first()
    subs_type = subs.subscription_type
    return subs_type.id


@sync_to_async()
def get_solved_task_by_user_n_chapter(user: User, chapter_id: int):
    """Get solved task by user and chapter."""
    task_solved = TaskSolved.objects.filter(
        user=user, task__number_of_chapter=chapter_id).first()
    return task_solved

from datetime import datetime
from pytz import timezone

@sync_to_async()
def get_days_from_the_start_of_subscription(user: User):
    """Get days from the start of subscription."""
    sub: Subscription = Subscription.objects.filter(user=user).first()
    now = datetime.now(timezone('Europe/Moscow'))
    days_passed = (now - sub.date_of_creation).days + 1
    return days_passed

async def choose_tasks_keyboard(user: User):
    """Generate choose tasks keyboard."""

    days_passed = await get_days_from_the_start_of_subscription(user)
    subs_type_id = await get_subscryption_type_id(user)
    if days_passed < 7:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 1) else '❌')
                                  + ' Глава 1', callback_data='chapter_1')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 2) else '❌') + ' Глава 2', callback_data='chapter_2')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 3) else '❌') + ' Глава 3', callback_data='chapter_3')],
            [InlineKeyboardButton(text='◀️ Назад', callback_data='main_menu')],
        ])
    elif days_passed < 30:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 1) else '❌') + ' Глава 1', callback_data='chapter_1')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 2) else '❌') + ' Глава 2', callback_data='chapter_2')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 3) else '❌') + ' Глава 3', callback_data='chapter_3')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 4) else '❌') + ' Глава 4', callback_data='chapter_4')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 5) else '❌') + ' Глава 5', callback_data='chapter_5')],
            [InlineKeyboardButton(text='◀️ Назад', callback_data='main_menu')],
        ])
    elif days_passed < 90:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 1) else '❌') + ' Глава 1', callback_data='chapter_1')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 2) else '❌') + ' Глава 2', callback_data='chapter_2')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 3) else '❌') + ' Глава 3', callback_data='chapter_3')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 4) else '❌') + ' Глава 4', callback_data='chapter_4')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 5) else '❌') + ' Глава 5', callback_data='chapter_5')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 6) else '❌') + ' Глава 6', callback_data='chapter_6')],
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, 7) else '❌') + ' Глава 7', callback_data='chapter_7')],
            [InlineKeyboardButton(text='◀️ Назад', callback_data='main_menu')],
        ])

    return keyboard


@sync_to_async()
def is_task_solved(user: User, task: Task):
    """Check if task is solved."""
    task_solved = TaskSolved.objects.filter(user=user, task=task).first()
    return task_solved


async def chapter_keyboard(user: User, task: Task):
    """Generate chapter keyboard."""

    if await is_task_solved(user, task):
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='💬 Обусдить главу',
                                  callback_data=f'discuss_{task.id}')],
            [InlineKeyboardButton(
                text='👁 Посмотреть свой ответ', callback_data=f'view_answer_{task.id}')],
            [InlineKeyboardButton(text='◀️ Назад', callback_data='tasks')],
        ])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔍 Выполнить задание',
                                  callback_data=f'complete_task_{task.id}')],
            [InlineKeyboardButton(text='💬 Обусдить главу',
                                  callback_data=f'discuss_{task.id}')],
            [InlineKeyboardButton(text='◀️ Назад', callback_data='tasks')],
        ])
    return keyboard
