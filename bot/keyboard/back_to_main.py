from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def back_to_main_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")],
    ])
    return keyboard
