from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.user.models import User, Subscription
from asgiref.sync import sync_to_async
import logging


async def main_menu(user: User) -> InlineKeyboardMarkup:
    """Generate main menu for user."""

    try:
        try:
            subs = await Subscription.objects.aget(user=user)
            q = True
        except:
            q = False

        if not q:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Краткая методичка",
                                     callback_data="short_methodics")],
                [InlineKeyboardButton(
                    text="Методичка", callback_data="methodics")],
                [InlineKeyboardButton(text="Книга", callback_data="book")],
                [InlineKeyboardButton(text="Оформить подписку",
                                     callback_data="go_on_subscription")],
                [InlineKeyboardButton(text="Помощь", callback_data="help")],
            ])
        else:
            keyboard = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="Краткая методичка",
                                     callback_data="short_methodics")],
                [InlineKeyboardButton(
                    text="Методичка", callback_data="methodics")],
                [InlineKeyboardButton(text="Книга", callback_data="book")],
                [InlineKeyboardButton(text="Личный кабинет",
                                     callback_data="user_lk")],
                [InlineKeyboardButton(text="Помощь", callback_data="help")],
            ])

        return keyboard
    except Exception as e:
        logging.error(f'Error while generating main menu: {e}')
