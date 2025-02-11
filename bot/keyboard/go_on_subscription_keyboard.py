from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from api.user.models import ThemePool


async def go_on_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="🕰 1 неделя", callback_data="1_week_subscription_purchase")],
            [InlineKeyboardButton(
                text="⏰ 1 месяц ⏰", callback_data="1_month_subscription_purchase")],
            [InlineKeyboardButton(
                text="🕐 🕐 3 месяца 🕐 🕐", callback_data="3_month_subscription_purchase")],
            [InlineKeyboardButton(
                text="◀️ Назад", callback_data="main_menu")],
        ],
    )
    return keyboard


async def subscription_purchased_keyboard():

    arr = []
    async for el in ThemePool.objects.all():
        arr.append([InlineKeyboardButton(text=el.name, callback_data=f"theme_{el.id}")])

    keyboard = InlineKeyboardMarkup(inline_keyboard=arr)
    return keyboard

async def theme_chosen_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⏰ Поставить напоминания", callback_data="notifications_settings")],
        [InlineKeyboardButton(text="⏭ Оставить отзыв", callback_data="rate_subscription")],
    ])
    return keyboard

async def rate_subscription_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐️", callback_data="rate_1")],
        [InlineKeyboardButton(text="⭐️⭐️", callback_data="rate_2")],
        [InlineKeyboardButton(text="⭐️⭐️⭐️", callback_data="rate_3")],
        [InlineKeyboardButton(text="⭐️⭐️⭐️⭐️", callback_data="rate_4")],
        [InlineKeyboardButton(text="⭐️⭐️⭐️⭐️⭐️", callback_data="rate_5")],
    ][::-1])
    return keyboard