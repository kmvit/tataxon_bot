from __future__ import absolute_import
import os
from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tataxon_bot.settings')

app = Celery("tataxon_bot")

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# проверка
@app.task
def add(x, y):
    return x / y
