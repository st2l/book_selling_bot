from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.user.models import User, Task, Subscription, TaskSolved
from asgiref.sync import sync_to_async


@sync_to_async()
def get_subscryption_type_id(user: User):
    """Get user subscryption type id."""
    subs: Subscription = Subscription.objects.filter(user=user).first()
    subs_type = subs.subscription_type
    return subs_type.id


async def choose_tasks_keyboard(user: User):
    """Generate choose tasks keyboard."""

    subs_type_id = await get_subscryption_type_id(user)
    if subs_type_id == 1:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Глава 1', callback_data='chapter_1')],
            [InlineKeyboardButton(text='Глава 2', callback_data='chapter_2')],
            [InlineKeyboardButton(text='Глава 3', callback_data='chapter_3')],
            [InlineKeyboardButton(text='🔙 Назад', callback_data='main_menu')],
        ])
    elif subs_type_id == 2:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Глава 1', callback_data='chapter_1')],
            [InlineKeyboardButton(text='Глава 2', callback_data='chapter_2')],
            [InlineKeyboardButton(text='Глава 3', callback_data='chapter_3')],
            [InlineKeyboardButton(text='Глава 4', callback_data='chapter_4')],
            [InlineKeyboardButton(text='Глава 5', callback_data='chapter_5')],
            [InlineKeyboardButton(text='🔙 Назад', callback_data='main_menu')],
        ])
    elif subs_type_id == 3:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Глава 1', callback_data='chapter_1')],
            [InlineKeyboardButton(text='Глава 2', callback_data='chapter_2')],
            [InlineKeyboardButton(text='Глава 3', callback_data='chapter_3')],
            [InlineKeyboardButton(text='Глава 4', callback_data='chapter_4')],
            [InlineKeyboardButton(text='Глава 5', callback_data='chapter_5')],
            [InlineKeyboardButton(text='Глава 6', callback_data='chapter_6')],
            [InlineKeyboardButton(text='Глава 7', callback_data='chapter_7')],
            [InlineKeyboardButton(text='🔙 Назад', callback_data='main_menu')],
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
            [InlineKeyboardButton(text='🔙 Назад', callback_data='tasks')],
        ])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🔍 Выполнить задание',
                                  callback_data=f'complete_task_{task.id}')],
            [InlineKeyboardButton(text='🔙 Назад', callback_data='tasks')],
        ])
    return keyboard
