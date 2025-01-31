from api.user.models import User
from aiogram.types import Message, CallbackQuery


async def identify_user(message: Message | CallbackQuery):
    user, is_new = await User.objects.aget_or_create(
        pk=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        },
    )

    return user, is_new
