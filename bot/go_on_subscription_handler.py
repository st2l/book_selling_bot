from __future__ import annotations

from typing import TYPE_CHECKING
import os
import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from api.user.models import User, Methodic, History
from bot.keyboard import choose_three_methodics_keyboard, methodic_1_keyboard, \
    back_to_main_keyboard, methodic_2_keyboard, methodic_3_keyboard, methodic_all_keyboard

from utils import get_bot_text, identify_user

from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery, FSInputFile
from asgiref.sync import sync_to_async

go_on_subscription_router = Router()