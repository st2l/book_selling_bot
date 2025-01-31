from __future__ import annotations

import logging.config
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from api.config.logging import LOGGING
from bot.config.bot import RUNNING_MODE, TELEGRAM_API_TOKEN, RunningMode
from bot.handlers import router
from bot.short_methodics_handler import short_methodics_router

# FOR INITIAL CREATION OF DATABASE
from asgiref.sync import sync_to_async
from api.user.models import BotText

# LOGGING
logging.config.dictConfig(LOGGING)
logger = logging.getLogger(__name__)

bot = Bot(TELEGRAM_API_TOKEN)

dispatcher = Dispatcher()
dispatcher.include_router(router)
dispatcher.include_router(short_methodics_router)


async def set_bot_commands() -> None:
    await bot.set_my_commands(
        [
            BotCommand(command="/start", description="Start the bot!"),
        ],
    )


async def create_all_default_bot_texts() -> None:
    try:
        # start pain text
        try:
            q = await BotText.objects.aget(name='start_text_pain')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="start_text_pain", text="Опишите мне вашу боль",
            )

        # Выделение боли и уточняющий вопрос
        try:
            q = await BotText.objects.aget(name='Выделение боли и уточняющий вопрос')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Выделение боли и уточняющий вопрос", text="О да... {}... Я правильно понял, что ты хочешь решить {}?",
            )

        # Стартовое сообщение и рекомендацию по использованию подписки
        try:
            q = await BotText.objects.aget(name='Стартовое сообщение и рекомендацию по использованию подписки')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Стартовое сообщение и рекомендацию по использованию подписки",
                text="Предлагаю тебе выбрать способ решения, но прежде чем выбрать прочти до конца. (Краткая рекомендация по использованию подпиской)",
            )
        
        # Краткая информация для краткой методички
        try:
            q = await BotText.objects.aget(name='Краткая информация для краткой методички')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Краткая информация для краткой методички",
                text="Эта краткая методичка поможет вам решить вашу боль!",
            )
    except Exception as e:
        logging.error(f"Error while creating default bot texts: {e}")


@dispatcher.startup()
async def on_startup() -> None:
    await set_bot_commands()

    # CREATION OF DEFAULT BOT TEXTS
    await create_all_default_bot_texts()


def run_polling() -> None:
    dispatcher.run_polling(bot)


def run_webhook() -> None:
    msg = "Webhook mode is not implemented yet"
    raise NotImplementedError(msg)


if __name__ == "__main__":
    if RUNNING_MODE == RunningMode.LONG_POLLING:
        run_polling()
    elif RUNNING_MODE == RunningMode.WEBHOOK:
        run_webhook()
    else:
        logger.error("Unknown running mode")
        sys.exit(1)
