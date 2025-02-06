from schedulers import check_and_send_notifications, check_and_send_messages, check_and_notify_subscriptions, check_and_send_dialogs
from apscheduler.schedulers.asyncio import AsyncIOScheduler

def start_scheduler():
    # TODO: change for production

    scheduler = AsyncIOScheduler()
    scheduler.add_job(check_and_send_notifications, 'interval', minutes=1)
    scheduler.add_job(check_and_send_messages, 'cron', minute='*', second=30)
    scheduler.add_job(check_and_notify_subscriptions, 'cron', hour=0, minute=0)
    scheduler.add_job(check_and_send_dialogs, 'cron', hour='10,22', minute=0)


    scheduler.start()