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
    # Calculate number of weeks (rounding up)
    weeks_passed = (days_passed + 6) // 7  # Adding 6 to round up division
    
    # Create a list of keyboard buttons based on weeks passed
    keyboard_buttons = []
    for chapter in range(1, weeks_passed + 1):
        keyboard_buttons.append(
            [InlineKeyboardButton(text=('✔' if await get_solved_task_by_user_n_chapter(user, chapter) else '❌') + 
                                  f' Глава {chapter}', callback_data=f'chapter_{chapter}')]
        )
    
    # Add back button
    keyboard_buttons.append([InlineKeyboardButton(text='◀️ Назад', callback_data='main_menu')])
    
    # Create keyboard with generated buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=keyboard_buttons)

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
