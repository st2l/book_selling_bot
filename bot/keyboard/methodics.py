from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asgiref.sync import sync_to_async
from api.user.models import Methodic


@sync_to_async()
def get_methodics():
    methodics_1 = Methodic.objects.get(id=1)
    methodics_2 = Methodic.objects.get(id=2)
    methodics_3 = Methodic.objects.get(id=3)
    return methodics_1, methodics_2, methodics_3


async def choose_three_methodics_keyboard() -> InlineKeyboardMarkup:
    methodics_1, methodics_2, methodics_3 = await get_methodics()
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=methodics_1.name, callback_data="methodic_1")],
        [InlineKeyboardButton(text=methodics_2.name, callback_data="methodic_2")],
        [InlineKeyboardButton(text=methodics_3.name, callback_data="methodic_3")],
        [InlineKeyboardButton(text="💰 Приобрести все! 💰",
                              callback_data="methodic_all")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="main_menu")],
    ])
    return keyboard


async def methodic_1_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💵 Купить", callback_data="methodic_1_purchase")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="methodics")],
    ])
    return keyboard


async def methodic_2_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💵 Купить", callback_data="methodic_2_purchase")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="methodics")],
    ])
    return keyboard


async def methodic_3_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💵 Купить", callback_data="methodic_3_purchase")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="methodics")],
    ])
    return keyboard

async def methodic_all_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="💵 Купить все", callback_data="methodic_all_purchase")],
        [InlineKeyboardButton(text="◀️ Назад", callback_data="methodics")],
    ])
    return keyboard