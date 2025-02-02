from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def choose_three_methodics_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Методичка 1", callback_data="methodic_1")],
        [InlineKeyboardButton(text="Методичка 2", callback_data="methodic_2")],
        [InlineKeyboardButton(text="Методичка 3", callback_data="methodic_3")],
        [InlineKeyboardButton(text="Приобрести все!",
                              callback_data="methodic_all")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")],
    ])
    return keyboard


async def methodic_1_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💵 Купить", callback_data="methodic_1_purchase")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="methodics")],
    ])
    return keyboard


async def methodic_2_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💵 Купить", callback_data="methodic_2_purchase")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="methodics")],
    ])
    return keyboard


async def methodic_3_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💵 Купить", callback_data="methodic_3_purchase")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="methodics")],
    ])
    return keyboard
