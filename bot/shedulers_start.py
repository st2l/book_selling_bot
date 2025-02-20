from bot.schedulers import check_and_send_notifications, check_and_send_messages, check_and_notify_subscriptions, check_and_send_dialogs, check_and_send_rating_requests
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def start_scheduler():
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    scheduler.add_job(check_and_send_notifications, 'interval', minutes=1)
    scheduler.add_job(check_and_send_messages, 'cron', minute='*', second=30)
    scheduler.add_job(check_and_notify_subscriptions, 'interval', minutes=1)
    # Заменим на проверку каждую минуту
    scheduler.add_job(check_and_send_dialogs, 'interval', minutes=1)
    scheduler.add_job(check_and_send_rating_requests, 'interval', minutes=1)

    scheduler.start()