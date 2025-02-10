from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def subscription_renewal_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🕰 1 неделя", callback_data="renew_1week")],
            [InlineKeyboardButton(text="⏰ 1 месяц ⏰", callback_data="renew_1month")],
            [InlineKeyboardButton(text="🕐 🕐 3 месяца 🕐 🕐", callback_data="renew_3months")],
            [InlineKeyboardButton(text="◀️ Назад", callback_data="user_lk")],
        ],
    )
    return keyboard 