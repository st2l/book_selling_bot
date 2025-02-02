from __future__ import annotations

import logging.config
import sys

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand

from api.config.logging import LOGGING
from bot.config.bot import RUNNING_MODE, TELEGRAM_API_TOKEN, RunningMode

# ROUTERS
from bot.handlers import router
from bot.short_methodics_handler import short_methodics_router
from bot.main_menu import main_menu_router
from bot.methodics_handler import methodics_router
from bot.book_handler import book_router

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
dispatcher.include_router(main_menu_router)
dispatcher.include_router(methodics_router)
dispatcher.include_router(book_router)


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

        # Главное меню
        try:
            q = await BotText.objects.aget(name='Главное меню')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Главное меню",
                text="Главное меню",
            )

        # Оплата краткой методички
        try:
            q = await BotText.objects.aget(name='Оплата краткой методички')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Оплата краткой методички",
                text="Оплатите краткую методичку удобным вам способом!",
            )

        # Краткая методичка куплена успешно
        try:
            q = await BotText.objects.aget(name='Краткая методичка куплена успешно')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Краткая методичка куплена успешно",
                text="Краткая методичка куплена успешно!",
            )

        # Информация для методичек
        try:
            q = await BotText.objects.aget(name='Информация для методичек')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Информация для методичек",
                text="Информация для методичек!!",
            )

        # Методичка куплена успешно
        try:
            q = await BotText.objects.aget(name='Методичка куплена успешно')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Методичка куплена успешно",
                text="Методичка куплена успешно!!",
            )

        # Описание при покупке всех методичек
        try:
            q = await BotText.objects.aget(name='Описание при покупке всех методичек')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Описание при покупке всех методичек",
                text="Описание при покупке всех методичек!!",
            )
        
        # Успешная покупка книги
        try:
            q = await BotText.objects.aget(name='Успешная покупка книги')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Успешная покупка книги",
                text="Успешная покупка книги!!",
            )
    except Exception as e:
        logging.error(f"Error while creating default bot texts: {e}")


async def create_short_methodic_default():
    try:
        from api.user.models import ShortMethodic
        try:
            q = await ShortMethodic.objects.aget(id=1)
        except:
            await ShortMethodic.objects.acreate(
                name='Краткая методичка',
                price=100,
                description='Краткая методичка для решения вашей боли',
            )
    except Exception as e:
        logging.error(f"Error while creating default short methodic: {e}")


async def create_methodic_default():
    try:
        from api.user.models import Methodic
        try:
            q = await Methodic.objects.aget(id=1)
        except:
            await Methodic.objects.acreate(
                name='Методичка 1',
                price=200,
                description='Методичка для решения вашей боли',
            )

        try:
            q = await Methodic.objects.aget(id=2)
        except:
            await Methodic.objects.acreate(
                name='Методичка 2',
                price=200,
                description='Методичка для решения вашей боли 2',
            )

        try:
            q = await Methodic.objects.aget(id=3)
        except:
            await Methodic.objects.acreate(
                name='Методичка 3',
                price=200,
                description='Методичка для решения вашей боли 3',
            )
    except Exception as e:
        logging.error(f"Error while creating default methodic: {e}")


async def create_default_book():
    try:
        from api.user.models import Book
        try:
            q = await Book.objects.aget(id=1)
        except:
            await Book.objects.acreate(
                name='Книга',
                price=200,
                description='Книга для решения вашей боли',
            )
    except Exception as e:
        logging.error(f"Error while creating default book: {e}")


@dispatcher.startup()
async def on_startup() -> None:
    await set_bot_commands()

    # CREATION OF DEFAULT BOT TEXTS
    await create_all_default_bot_texts()

    # CREATION OF DEFAULT SHORT METHODIC
    await create_short_methodic_default()

    # CREATION OF DEFAULT METHODIC
    await create_methodic_default()

    # CREATION OF DEFAULT BOOK
    await create_default_book()


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
