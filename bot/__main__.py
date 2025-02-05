from __future__ import annotations

import logging.config
import sys

from aiogram import Dispatcher
from aiogram.types import BotCommand

from bot.bot_instance import bot
from bot.config.bot import RUNNING_MODE, RunningMode

# ROUTERS
from bot.handlers import router
from bot.short_methodics_handler import short_methodics_router
from bot.main_menu import main_menu_router
from bot.methodics_handler import methodics_router
from bot.book_handler import book_router
from bot.help_handler import help_router
from bot.go_on_subscription_handler import go_on_subscription_router
from bot.user_lk_handler import user_lk_router
from bot.tasks_handler import tasks_router

# FOR INITIAL CREATION OF DATABASE
from asgiref.sync import sync_to_async
from api.user.models import BotText

# FOR SCHEDULER
from schedulers import check_and_send_notifications, \
    check_and_notify_subscriptions, \
    check_and_send_messages

from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from api.user.models import Notification, User

logger = logging.getLogger(__name__)

dispatcher = Dispatcher()
dispatcher.include_router(router)
dispatcher.include_router(short_methodics_router)
dispatcher.include_router(main_menu_router)
dispatcher.include_router(methodics_router)
dispatcher.include_router(book_router)
dispatcher.include_router(help_router)
dispatcher.include_router(go_on_subscription_router)
dispatcher.include_router(user_lk_router)
dispatcher.include_router(tasks_router)


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

        # Помощь
        try:
            q = await BotText.objects.aget(name='Помощь')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Помощь",
                text="Помощь текст!!",
            )

        # Текст при оформлении подписки
        try:
            q = await BotText.objects.aget(name='Текст при оформлении подписки')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Текст при оформлении подписки",
                text="Текст при оформлении подписки!!",
            )

        # Подписка успешно оформлена
        try:
            q = await BotText.objects.aget(name='Подписка успешно оформлена')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Подписка успешно оформлена",
                text="Подписка успешно оформлена!!",
            )

        # Тема успешно выбрана
        try:
            q = await BotText.objects.aget(name='Тема успешно выбрана')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Тема успешно выбрана",
                text="Тема успешно выбрана!!",
            )

        # Оцените подписку
        try:
            q = await BotText.objects.aget(name='Оцените подписку')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Оцените подписку",
                text="Оцените подписку!!",
            )

        # Спасибо за оценку
        try:
            q = await BotText.objects.aget(name='Спасибо за оценку')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Спасибо за оценку",
                text="Спасибо за оценку!!",
            )

        # История покупок
        try:
            q = await BotText.objects.aget(name='История покупок')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="История покупок",
                text="История покупок!!",
            )

        # Изменить интересующие темы
        try:
            q = await BotText.objects.aget(name='Изменить интересующие темы')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Изменить интересующие темы",
                text="Изменить интересующие темы!!",
            )

        # Изменить напоминания
        try:
            q = await BotText.objects.aget(name='Изменить напоминания')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Изменить напоминания",
                text="Изменить напоминания!!",
            )

        # Добавить текст напоминанию
        try:
            q = await BotText.objects.aget(name='Добавить текст напоминанию')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Добавить текст напоминанию",
                text="Введите текст для вашего напоминания!!",
            )

        # Добавить время напоминания
        try:
            q = await BotText.objects.aget(name='Добавить время напоминания')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Добавить время напоминания",
                text="Введите время для напоминания в формате ЧЧ:ММ!!",
            )

        # Напоминание добавлено
        try:
            q = await BotText.objects.aget(name='Напоминание добавлено')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Напоминание добавлено",
                text="Напоминание добавлено!!",
            )

        # Напоминание добавлено
        try:
            q = await BotText.objects.aget(name='Текст уведомления изменен')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Текст уведомления изменен",
                text="Текст уведомления изменен!!",
            )

        # Уведомление удалено
        try:
            q = await BotText.objects.aget(name='Уведомление удалено')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Уведомление удалено",
                text="Уведомление удалено!!",
            )

        # Задания
        try:
            q = await BotText.objects.aget(name='Задания')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Задания",
                text="Задания!!",
            )

        # Введите решение задачи
        try:
            q = await BotText.objects.aget(name='Введите решение задачи')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Введите решение задачи",
                text="Введите решение задачи!!",
            )

        # Задача решена успешно
        try:
            q = await BotText.objects.aget(name='Задача решена успешно')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Задача решена успешно",
                text="Задача решена успешно!!",
            )

        # Обсуждение главы
        try:
            q = await BotText.objects.aget(name='Обсуждение главы')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Обсуждение главы",
                text="Обсуждение главы!!",
            )

        # Время уведомления изменено
        try:
            q = await BotText.objects.aget(name='Время уведомления изменено')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Время уведомления изменено",
                text="Время уведомления изменено!!",
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


async def create_default_themes():
    try:
        from api.user.models import ThemePool
        try:
            q = await ThemePool.objects.aget(id=1)
        except:
            await ThemePool.objects.acreate(
                name='Саморазвитие',
            )

        try:
            q = await ThemePool.objects.aget(id=2)
        except:
            await ThemePool.objects.acreate(
                name='Продуктивность',
            )

        try:
            q = await ThemePool.objects.aget(id=3)
        except:
            await ThemePool.objects.acreate(
                name='Управление временем',
            )
    except Exception as e:
        logging.error(f"Error while creating default themes: {e}")


async def create_default_subscriptions():
    try:
        from api.user.models import SubscriptionDetails
        try:
            q = await SubscriptionDetails.objects.aget(id=1)
        except:
            await SubscriptionDetails.objects.acreate(
                name='1 неделя',
                price=200,
                description='1 недельная подписка',
                days=7,
            )

        try:
            q = await SubscriptionDetails.objects.aget(id=2)
        except:
            await SubscriptionDetails.objects.acreate(
                name='1 месяц',
                price=500,
                description='1 месячная подписка',
                days=30,
            )

        try:
            q = await SubscriptionDetails.objects.aget(id=3)
        except:
            await SubscriptionDetails.objects.acreate(
                name='3 месяца',
                price=1000,
                description='3 месячная подписка',
                days=90,
            )
    except Exception as e:
        logging.error(f"Error while creating default subscriptions: {e}")


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_notifications, 'interval', minutes=1)
    scheduler.add_job(check_and_send_messages, 'interval', minutes=1)
    scheduler.add_job(check_and_notify_subscriptions, 'cron', hour=0, minute=0)
    scheduler.start()


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

    # CREATION OF DEFAULT SUBSCRIPTIONS
    await create_default_subscriptions()

    # CREATION OF DEFAULT THEMES
    await create_default_themes()

    # START SCHEDULER
    start_scheduler()


async def run_polling() -> None:
    await dispatcher.start_polling(bot)


def run_webhook() -> None:
    msg = "Webhook mode is not implemented yet"
    raise NotImplementedError(msg)


async def main():
    start_scheduler()
    await run_polling()

if __name__ == "__main__":
    import asyncio

    asyncio.run(main())

    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # loop.create_task(start_scheduler())
    # loop.run_forever()
    # # loop.close()
    # # start_scheduler()

    # if RUNNING_MODE == RunningMode.LONG_POLLING:
    #     run_polling()
    # elif RUNNING_MODE == RunningMode.WEBHOOK:
    #     run_webhook()
    # else:
    #     logger.error("Unknown running mode")
    #     sys.exit(1)
