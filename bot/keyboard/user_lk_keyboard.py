from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.user.models import User, Subscription, History, ThemePool, Notification
from asgiref.sync import sync_to_async


async def user_lk_keyboard(user: User, subs: Subscription | None) -> InlineKeyboardMarkup:
    """Generate user lk keyboard."""
    if subs:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⏰ Изменить напоминания",
                                  callback_data="notifications_settings")],
            [InlineKeyboardButton(
                text="Изменить интересующие темы", callback_data="change_theme")],
            [InlineKeyboardButton(text="🔁 История покупок",
                                  callback_data="purchase_history")],
            [InlineKeyboardButton(text="◀️ Назад",
                                  callback_data="main_menu")]
        ])
    else:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🔁 История покупок",
                                  callback_data="purchase_history")],
            [InlineKeyboardButton(text="◀️ Назад",
                                  callback_data="main_menu")]
        ])

    return keyboard


@sync_to_async()
def get_arr(user: User):
    arr = []
    for el in History.objects.filter(user=user):
        if el.methodic:
            arr.append([InlineKeyboardButton(
                text=el.methodic.name, callback_data=f"history_{el.id}")])
        elif el.short_methodic:
            arr.append([InlineKeyboardButton(
                text=el.short_methodic.name, callback_data=f"history_{el.id}")])
        elif el.book:
            arr.append([InlineKeyboardButton(
                text=el.book.name, callback_data=f"history_{el.id}")])
    return arr


async def history_keyboard(user: User) -> InlineKeyboardMarkup:
    """Generate history keyboard."""

    arr = await get_arr(user)
    arr.append([InlineKeyboardButton(text="◀️ Назад", callback_data="user_lk")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=arr)
    return keyboard


async def change_theme_keyboard():

    arr = []
    async for el in ThemePool.objects.all():
        arr.append([InlineKeyboardButton(
            text=el.name, callback_data=f"changetheme_{el.id}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=arr)
    return keyboard


@sync_to_async()
def get_notifications(user: User):
    notifications = Notification.objects.filter(user=user).all()
    can_be_more = len(notifications) < 3

    kb = []
    for el in notifications:
        kb.append([
            InlineKeyboardButton(
                text=el.text, callback_data=f"view_notification_{el.id}"),
        ])
    return kb, can_be_more


async def notifications_settings_keyboard(user: User):

    arr, can_be_more = await get_notifications(user)
    if can_be_more:
        arr.append([InlineKeyboardButton(
            text="➕ Добавить напоминание", callback_data="add_notification")])
    arr.append([InlineKeyboardButton(text='◀️ Назад', callback_data='user_lk')])

    return InlineKeyboardMarkup(inline_keyboard=arr)


async def view_notification_keyboard(notification: Notification):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="🔁 Изменить текст", callback_data=f"change_text_notification_{notification.id}")],
        [InlineKeyboardButton(
            text="🔁 Изменить время", callback_data=f"change_time_notification_{notification.id}")],
        [InlineKeyboardButton(
            text="❌", callback_data=f"delete_notification_{notification.id}")],
        [InlineKeyboardButton(
            text="◀️ Назад", callback_data="notifications_settings")]
    ])
