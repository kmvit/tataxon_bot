import os
import sys

import httpx

from tataxon_bot.celery import app

try:
    from rss_parser import rss_parser
except ModuleNotFoundError:
    # Добавляем путь к родительскому каталогу в sys.path
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    )
    from rss_parser import rss_parser

@app.task
def parser():
    rss_parser(httpx_client = httpx.AsyncClient())#insert_to_db()
    print('Парсер отработал')
    
    # https://habr.com/ru/articles/820073/
    # https://code.tutsplus.com/ru/using-celery-with-django-for-background-task-processing--cms-28732t
    
    # 1. запускаем redis командой
    # #sudo docker run -d --name redis-test -p 6380:6379 \
    #    -v /path/to/redisconf/redis.conf:/redis.conf \
    #    redis redis-server /redis.conf
    
    # 2. в другом терминале запускаем работника Celery, находясь evo@evo:~/Dev/tataxon_bot/tataxon_bot$
    # celery -A tataxon_bot.celery worker --loglevel=INFO --pidfile=''
    
    # 3. в другом окне терминала вызываем планировщика, находясь evo@evo:~/Dev/tataxon_bot/tataxon_bot$
    # celery -A tataxon_bot beat --loglevel=INFO
    
    # Результаты, отображающиеся во втором терминале
    # [2024-10-28 22:39:13,711: INFO/MainProcess] Task api.tasks.parser[bd0a1ae3-7378-4a76-8b29-5de1dc81ce74] received
    # [2024-10-28 22:39:13,729: WARNING/ForkPoolWorker-15] /home/evo/Dev/tataxon_bot/tataxon_bot/api/tasks.py:19: RuntimeWarning: coroutine 'rss_parser' was never awaited
    # rss_parser(httpx_client = httpx.AsyncClient())#insert_to_db()

    # [2024-10-28 22:39:13,730: WARNING/ForkPoolWorker-15] Парсер отработал
    # [2024-10-28 22:39:13,731: INFO/ForkPoolWorker-15] Task api.tasks.parser[bd0a1ae3-7378-4a76-8b29-5de1dc81ce74] succeeded in 0.019534987999577424s: None
    # [2024-10-28 22:40:00,001: INFO/MainProcess] Task api.tasks.parser[eab7a248-8492-4b9b-8c45-e1c930843bc1] received
    # [2024-10-28 22:40:00,021: WARNING/ForkPoolWorker-15] Парсер отработал
    # [2024-10-28 22:40:00,022: INFO/ForkPoolWorker-15] Task api.tasks.parser[eab7a248-8492-4b9b-8c45-e1c930843bc1] succeeded in 0.019957196000177646s: None
