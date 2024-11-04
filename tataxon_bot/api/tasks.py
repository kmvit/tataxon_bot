import os
import sys

import httpx
import asyncio

from api.models import Advertisement
from tataxon_bot.celery import app

try:
    from db_saver import insert_to_db
    from rss_parser import rss_parser
except ModuleNotFoundError:
    # Добавляем путь к родительскому каталогу в sys.path
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    )
    from db_saver import insert_to_db
    from rss_parser import rss_parser

@app.task
def parser():
    """
    Фоновая задача, происходит парсинг данных и добавление их в базу.
    """
    ads_pars = asyncio.run(rss_parser(httpx_client = httpx.AsyncClient()))
    insert_to_db(ads_pars)
