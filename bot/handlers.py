from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Router
from aiogram.filters import Command

from api.user.models import User

from utils import get_bot_text

if TYPE_CHECKING:
    from aiogram.types import Message

router = Router()


@router.message(Command(commands=["start"]))
async def handle_start_command(message: Message) -> None:
    if message.from_user is None:
        return

    _, is_new = await User.objects.aget_or_create(
        pk=message.from_user.id,
        defaults={
            "username": message.from_user.username,
            "first_name": message.from_user.first_name,
            "last_name": message.from_user.last_name,
        },
    )
        
    await message.answer(text=await get_bot_text(name='start_text_pain'))


@router.message(Command(commands=["id"]))
async def handle_id_command(message: Message) -> None:
    if message.from_user is None:
        return

    await message.answer(
        f"User Id: <b>{message.from_user.id}</b>\nChat Id: <b>{message.chat.id}</b>",
    )
