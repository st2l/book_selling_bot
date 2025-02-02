from api.user.models import User
from aiogram.types import Message, CallbackQuery


async def identify_user(message: Message | CallbackQuery):
    id_ = message.from_user.id
    first_name = message.from_user.first_name if message.from_user.first_name else "no_name"
    last_name = message.from_user.last_name if message.from_user.last_name else "no_name"

    user, is_new = await User.objects.aget_or_create(
        pk=message.from_user.id,
        defaults={
            "username": id_,
            "first_name": first_name,
            "last_name": last_name,
        },
    )

    return user, is_new
