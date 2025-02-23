from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from api.user.models import User, History, Subscription
from asgiref.sync import sync_to_async
import logging


async def main_menu(user: User) -> InlineKeyboardMarkup:
    """Generate main menu for user."""

    try:
        try:
            q = False
            async for el in History.objects.filter(user=user):
                q = True
                break
        except Exception as e:
            logging.error(f'Error while getting user subscription: {e}')
            q = False

        if not q:

            try:
                q = False
                async for el in Subscription.objects.filter(user=user):
                    q = True
                    break
            except Exception as e:
                logging.error(f'Error while getting user subscription: {e}')
                q = False

            if q:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[

                    [InlineKeyboardButton(text="🧠 Краткая методичка 🧠",
                                          callback_data="short_methodics")],
                    [InlineKeyboardButton(
                        text="🧠 Методичка 🧠", callback_data="methodics")],
                    [InlineKeyboardButton(text="📚 Книга 📚", callback_data="book")],
                    [InlineKeyboardButton(text="👤 Личный кабинет 👤",
                                          callback_data="user_lk")],
                    [InlineKeyboardButton(
                        text="💬 Помощь 💬", callback_data="help")],
                    [InlineKeyboardButton(
                        text="💪 Доступ к книге 💪", callback_data="tasks")],
                    [InlineKeyboardButton(text="🎯 Реферальная программа", callback_data="referral_program")],
                    [InlineKeyboardButton(text="💭 Чат единомышленников", callback_data="like_minded_chat")]
                ])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🧠 Краткая методичка 🧠",
                                          callback_data="short_methodics")],
                    [InlineKeyboardButton(
                        text="🧠 Методичка 🧠", callback_data="methodics")],
                    [InlineKeyboardButton(text="📚 Книга 📚", callback_data="book")],
                    [InlineKeyboardButton(text="💰 Оформить подписку 💰",
                                          callback_data="go_on_subscription")],
                    [InlineKeyboardButton(
                        text="💬 Помощь 💬", callback_data="help")],
                    [InlineKeyboardButton(text="🎯 Реферальная программа", callback_data="referral_program")],
                    [InlineKeyboardButton(text="💭 Чат единомышленников", callback_data="like_minded_chat")]
                ])
        else:
            try:
                q = False
                async for el in Subscription.objects.filter(user=user):
                    q = True
                    break
            except Exception as e:
                logging.error(f'Error while getting user subscription: {e}')
                q = False

            if q:

                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🧠 Краткая методичка 🧠",
                                          callback_data="short_methodics")],
                    [InlineKeyboardButton(
                        text="🧠 Методичка 🧠", callback_data="methodics")],
                    [InlineKeyboardButton(text="📚 Книга 📚", callback_data="book")],
                    [InlineKeyboardButton(text="👤 Личный кабинет 👤",
                                          callback_data="user_lk")],
                    [InlineKeyboardButton(
                        text="💬 Помощь 💬", callback_data="help")],
                    [InlineKeyboardButton(
                        text="💪 Доступ к книге 💪", callback_data="tasks")],
                    [InlineKeyboardButton(text="🎯 Реферальная программа", callback_data="referral_program")],
                    [InlineKeyboardButton(text="💭 Чат единомышленников", callback_data="like_minded_chat")]
                ])
            else:
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="🧠 Краткая методичка 🧠",
                                          callback_data="short_methodics")],
                    [InlineKeyboardButton(
                        text="🧠 Методичка 🧠", callback_data="methodics")],
                    [InlineKeyboardButton(text="📚 Книга 📚", callback_data="book")],
                    [InlineKeyboardButton(text="👤 Личный кабинет 👤",
                                          callback_data="user_lk")],
                    [InlineKeyboardButton(text="💰 Оформить подписку 💰",
                                          callback_data="go_on_subscription")],
                    [InlineKeyboardButton(
                        text="💬 Помощь 💬", callback_data="help")],
                    [InlineKeyboardButton(text="🎯 Реферальная программа", callback_data="referral_program")],
                    [InlineKeyboardButton(text="💭 Чат единомышленников", callback_data="like_minded_chat")]
                ])

        return keyboard
    except Exception as e:
        logging.error(f'Error while generating main menu: {e}')
