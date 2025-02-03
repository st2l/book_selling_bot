from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def go_on_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="1 неделя", callback_data="1_week_subscription_purchase")],
            [InlineKeyboardButton(
                text="1 месяц", callback_data="1_month_subscription_purchase")],
            [InlineKeyboardButton(
                text="3 месяца", callback_data="3_month_subscription_purchase")],
            [InlineKeyboardButton(
                text="🔙 Назад", callback_data="main_menu")],
        ],
    )
    return keyboard
