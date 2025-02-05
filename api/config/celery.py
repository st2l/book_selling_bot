from __future__ import annotations

from os import getenv

from api.config.application import TIME_ZONE
from celery import Celery
from celery.schedules import crontab

broker_url = getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

task_always_eager = getenv("CELERY_TASK_ALWAYS_EAGER",
                           "false").lower() == "true"
task_eager_propagates = getenv(
    "CELERY_TASK_EAGER_PROPAGATES", "false").lower() == "true"
task_ignore_result = getenv(
    "CELERY_TASK_IGNORE_RESULT", "false").lower() == "true"

timezone = TIME_ZONE
enable_utc = True

app = Celery("main")

app.conf.beat_schedule = {
    'check-and-send-notifications-every-minute': {
        'task': 'tasks.notifications.check_and_send_notifications',
        'schedule': crontab(minute='1'),
    },
}


app.config_from_object("api.config.celery")

app.autodiscover_tasks()
