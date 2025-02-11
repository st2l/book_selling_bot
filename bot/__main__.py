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
from bot.admin import admin_router
from bot.dialog_handler import dialog_router
from bot.like_minded_chat_handler import like_minded_chat_router
from bot.referral_handler import referral_router

# FOR INITIAL CREATION OF DATABASE
from asgiref.sync import sync_to_async
from api.user.models import BotText

# FOR SCHEDULER
from bot.shedulers_start import start_scheduler

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
dispatcher.include_router(admin_router)
dispatcher.include_router(dialog_router)
dispatcher.include_router(like_minded_chat_router)
dispatcher.include_router(referral_router)
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
                name="start_text_pain", text="Здравствуйте, {}! Опишите мне вашу боль",
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
                name="Стартовое сообщение и рекомендацию по использованию подпиской",
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
                text="<b>Главное меню</b>\n===============\n\nВыберите действие:",
            )

        # Оплата краткой методички
        # try:
        #     q = await BotText.objects.aget(name='Оплата краткой методички')
        # except:
        #     await sync_to_async(BotText.objects.create, thread_sensitive=True)(
        #         name="Оплата краткой методички",
        #         text="Оплатите краткую методичку удобным вам способом!",
        #     )

        # Краткая методичка куплена успешно
        try:
            q = await BotText.objects.aget(name='Краткая методичка куплена успешно')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Краткая методичка куплена успешно",
                text="✅<b>Краткая методичка куплена успешно!</b>✅\n\nТеперь вы можете использовать её для решения вашей боли!",
            )

        # Информация для методичек
        try:
            q = await BotText.objects.aget(name='Информация для методичек')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Информация для методичек",
                text="💴<b>Покупка методичек</b>💶\n\nВыберите интересующую методичку:",
            )

        # Методичка куплена успешно
        try:
            q = await BotText.objects.aget(name='Методичка куплена успешно')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Методичка куплена успешно",
                text="✅<b>Методичка куплена успешно!</b>✅\n\nТеперь вы можете использовать её для решения вашей боли!",
            )

        # Описание при покупке всех методичек
        try:
            q = await BotText.objects.aget(name='Описание при покупке всех методичек')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Описание при покупке всех методичек",
                text="💶<b>Покупка всех методичек</b>💸\n\nКаждая методичка обаладает своей уникальной информацией, которая способна помочь вам в решении вашей боли!",
            )

        # Успешная покупка книги
        try:
            q = await BotText.objects.aget(name='Успешная покупка книги')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Успешная покупка книги",
                text="✅<b>Успешная покупка книги!</b>✅\n\nТеперь вы можете использовать её для решения вашей боли!",
            )

        # Помощь
        try:
            q = await BotText.objects.aget(name='Помощь')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Помощь",
                text="💬<b>Помощь</b>💬\n\nЕсли у вас возникли трудности, пожалуйста, обратитесь в поддержку!",
            )

        # Текст при оформлении подписки
        try:
            q = await BotText.objects.aget(name='Текст при оформлении подписки')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Текст при оформлении подписки",
                text="💳<b>Оформление подписки</b>💳\n\n<i>(Чем дольше ваша подписка, тем больше уникального материала вы будуете получать ежедневно!)</i>\nВыберите подходящий для вас вариант подписки:",
            )

        # Подписка успешно оформлена
        try:
            q = await BotText.objects.aget(name='Подписка успешно оформлена')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Подписка успешно оформлена",
                text="✅<b>Подписка успешно оформлена!</b>✅\n\nТеперь вы можете использовать её для решения вашей боли!",
            )

        # Тема успешно выбрана
        try:
            q = await BotText.objects.aget(name='Тема успешно выбрана')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Тема успешно выбрана",
                text="🔍<b>Тема успешно выбрана!</b>🔍\n\nТеперь вы будете получать уникализированный контент по выбранной теме!",
            )

        # Оцените подписку
        try:
            q = await BotText.objects.aget(name='Оцените подписку')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Оцените подписку",
                text="💬<b>Оцените подписку</b>💬\n\nПожалуйста, оцените подписку, чтобы мы могли улучшить наш сервис!",
            )

        # Спасибо за оценку
        try:
            q = await BotText.objects.aget(name='Спасибо за оценку')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Спасибо за оценку",
                text="💖<b>Спасибо за оценку!</b>💖\n\nМы будем рады вашему отзыву!",
            )

        # История покупок
        try:
            q = await BotText.objects.aget(name='История покупок')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="История покупок",
                text="💳<b>История покупок</b>💳\n\nВы можете просматривать историю своих покупок, каждый материал, который вы приобрели, будет отображаться в этом разделе!",
            )

        # Изменить интересующие темы
        try:
            q = await BotText.objects.aget(name='Изменить интересующие темы')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Изменить интересующие темы",
                text="🔍<b>Изменение интересующих тем</b>🔍\n\nВы можете изменить интересующие вас темы, чтобы получать контент, который вам будет наиболее полезен!",
            )

        # Изменить напоминания
        try:
            q = await BotText.objects.aget(name='Изменить напоминания')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Изменить напоминания",
                text="🔔<b>Изменение напоминаний</b>🔔\n\nВы можете изменить напоминания, чтобы получать уведомления в удобное для вас время!",
            )

        # Добавить текст напоминанию
        try:
            q = await BotText.objects.aget(name='Добавить текст напоминанию')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Добавить текст напоминанию",
                text="🔔<b>Добавление текста напоминанию</b>🔔\n\nВведите текст для вашего напоминания:",
            )

        # Добавить время напоминания
        try:
            q = await BotText.objects.aget(name='Добавить время напоминания')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Добавить время напоминания",
                text="🔔<b>Добавление времени напоминанию</b>🔔\n\nВведите время для напоминания в формате ЧЧ:ММ (по МСК):",
            )

        # Напоминание добавлено
        try:
            q = await BotText.objects.aget(name='Напоминание добавлено')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Напоминание добавлено",
                text="✅<b>Напоминание добавлено!</b>✅\n\nТеперь вы будете получать уведомления в удобное для вас время!",
            )

        # Напоминание добавлено
        try:
            q = await BotText.objects.aget(name='Текст уведомления изменен')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Текст уведомления изменен",
                text="🔔<b>Изменение текста уведомления</b>🔔\n\nВведите новый текст для вашего напоминания:",
            )

        # Уведомление удалено
        try:
            q = await BotText.objects.aget(name='Уведомление удалено')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Уведомление удалено",
                text="♻️<b>Уведомление удалено!</b>♻️\n\nТеперь вы не будете получать уведомления!",
            )

        # Задания
        try:
            q = await BotText.objects.aget(name='Задания')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Задания",
                text="💪<b>Задания</b>💪\n\nВы можете просматривать задания, которые вам нужно выполнить, чтобы достичь своих целей!",
            )

        # Введите решение задачи
        try:
            q = await BotText.objects.aget(name='Введите решение задачи')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Введите решение задачи",
                text="💡<b>Введите решение задачи</b>💡\n\nВведите решение задачи:",
            )

        # Задача решена успешно
        try:
            q = await BotText.objects.aget(name='Задача решена успешно')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Задача решена успешно",
                text="✅<b>Задача решена успешно!</b>✅\n\nТеперь вы можете перейти к следующему заданию!",
            )

        # Обсуждение главы
        try:
            q = await BotText.objects.aget(name='Обсуждение главы')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Обсуждение главы",
                text="💬<b>Обсуждение главы</b>💬\n\nВы можете обсуждать главу, которая вам интересна, и получать ответы на свои вопросы!",
            )

        # Время уведомления изменено
        try:
            q = await BotText.objects.aget(name='Время уведомления изменено')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Время уведомления изменено",
                text="🔔<b>Изменение времени уведомления</b>🔔\n\nВведите новое время для вашего напоминания в формате ЧЧ:ММ (по МСК):",
            )

        # Add new default text for like-minded chat
        try:
            q = await BotText.objects.aget(name='Текст для чата единомышленников')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Текст для чата единомышленников",
                text="Присоединяйтесь к нашему чату единомышленников!\n\nЗдесь вы сможете общаться с людьми, которые разделяют ваши интересы и цели.",
            )
        
        # Add new default link for like-minded chat
        try:
            q = await BotText.objects.aget(name='Ссылка для чата единомышленников')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Ссылка для чата единомышленников",
                text="https://t.me/joinchat/AAAAAED000000000",
            )

        # Add referral program texts
        try:
            q = await BotText.objects.aget(name='Реферальная программа')
        except:
            await sync_to_async(BotText.objects.create, thread_sensitive=True)(
                name="Реферальная программа",
                text="Приглашайте друзей и получайте бонусы!\n\nЗа каждого купившего друга вы получите 7 дней подписки.",
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
                description='<b>Краткая методичка</b>\n\nЭта краткая методичка поможет вам решить вашу боль!',
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
                description='<b>Методичка 1</b>\n\nЭта методичка поможет вам решить вашу боль!',
            )

        try:
            q = await Methodic.objects.aget(id=2)
        except:
            await Methodic.objects.acreate(
                name='Методичка 2',
                price=200,
                description='<b>Методичка 2</b>\n\nЭта методичка поможет вам решить вашу боль!',
            )

        try:
            q = await Methodic.objects.aget(id=3)
        except:
            await Methodic.objects.acreate(
                name='Методичка 3',
                price=200,
                description='<b>Методичка 3</b>\n\nЭта методичка поможет вам решить вашу боль!',
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
                description='<b>Книга</b>\n\nЭта книга поможет вам решить вашу боль!',
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
                name='🧠 Саморазвитие 🧠',
            )

        try:
            q = await ThemePool.objects.aget(id=2)
        except:
            await ThemePool.objects.acreate(
                name='💼 Продуктивность 💼',
            )

        try:
            q = await ThemePool.objects.aget(id=3)
        except:
            await ThemePool.objects.acreate(
                name='🕒 Управление временем 🕒',
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
