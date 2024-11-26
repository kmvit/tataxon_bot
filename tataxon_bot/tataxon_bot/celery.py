from __future__ import absolute_import
import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tataxon_bot.settings')

app = Celery("tataxon_bot")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    'parser-every-three-hours': {
        'task': 'api.tasks.parser',
        'schedule': crontab(minute='*/1'),
        # crontab(minute='*/5') каждые 5 минут,
        # crontab(minute=0, hour='*/3') каждые 3 часа
    },
}
