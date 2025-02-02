from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


async def book_keyboard():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='💵 Купить', callback_data='book_purchase')],
        [InlineKeyboardButton(text='🔙 Назад', callback_data='main_menu')]
    ])

    return kb
