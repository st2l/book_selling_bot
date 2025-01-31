from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

async def short_methodics_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 Купить", callback_data="short_methodics_purchase")],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='main_menu')]
    ])
    return keyboard

async def short_methodics_purchase_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💵 Купить в ЮКасса", callback_data="short_methodics_yookassa")],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='short_methodics')]
    ])
    return keyboard
