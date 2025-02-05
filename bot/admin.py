from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from django.db.models import Count
from asgiref.sync import sync_to_async
from api.user.models import User, Subscription, Methodic, ShortMethodic, Book, History, Task, TaskSolved, SubscriptionDetails, Theme, ThemePool, Notification, Rating, SendMessage
from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()

admin_router = Router()


@admin_router.message(Command(commands=["admin"]))
async def handle_admin_command(message: Message, state: FSMContext) -> None:
    if message.from_user is None:
        return

    # Проверка на то, что пользователь администратор
    user_id = message.from_user.id
    is_admin = await check_if_user_is_admin(user_id)
    if not is_admin:
        await message.answer("У вас нет прав для доступа к этой команде.")
        return

    # Получение статистики
    stats = await get_database_statistics()

    # Получение URL админ панели из переменной окружения
    server_host = 'http://' + os.getenv("SERVER_HOST", "localhost") + ':8010'
    admin_url = f"{server_host}/admin/"

    # Формирование сообщения
    response_text = (
        f"<b>Админ панель</b>\n"
        f"Ссылка: <a href='{admin_url}'>Перейти в админ панель</a>\n\n"
        f"<b>Статистика базы данных:</b>\n"
        f"Пользователи: {stats['users']}\n"
        f"Подписки: {stats['subscriptions']}\n"
        f"Методики: {stats['methodics']}\n"
        f"Краткие методики: {stats['short_methodics']}\n"
        f"Книги: {stats['books']}\n"
        f"История: {stats['history']}\n"
        f"Задания: {stats['tasks']}\n"
        f"Решенные задания: {stats['tasks_solved']}\n"
        f"Детали подписок: {stats['subscription_details']}\n"
        f"Темы: {stats['themes']}\n"
        f"Уведомления: {stats['notifications']}\n"
        f"Оценки: {stats['ratings']}\n"
        f"Сообщения: {stats['send_messages']}\n"
    )

    await message.answer(text=response_text, parse_mode='HTML')


@sync_to_async()
def check_if_user_is_admin(user_id: int) -> bool:
    try:
        user = User.objects.get(id=user_id)
        return user.is_staff or user.is_superuser
    except User.DoesNotExist:
        return False


@sync_to_async()
def get_database_statistics():
    return {
        "users": User.objects.count(),
        "subscriptions": Subscription.objects.count(),
        "methodics": Methodic.objects.count(),
        "short_methodics": ShortMethodic.objects.count(),
        "books": Book.objects.count(),
        "history": History.objects.count(),
        "tasks": Task.objects.count(),
        "tasks_solved": TaskSolved.objects.count(),
        "subscription_details": SubscriptionDetails.objects.count(),
        "themes": Theme.objects.count(),
        "notifications": Notification.objects.count(),
        "ratings": Rating.objects.count(),
        "send_messages": SendMessage.objects.count(),
    }
