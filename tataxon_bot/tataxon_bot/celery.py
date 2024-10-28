from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tataxon_bot.settings')

app = Celery("tataxon_bot")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parser-every-single-minute': {
        'task': 'api.tasks.parser',
        'schedule': crontab(),  # crontab(minute='*/15') каждые 15 минут
    },
}
