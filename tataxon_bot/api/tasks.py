import asyncio
import logging
import os
import sys

import httpx
from asgiref.sync import async_to_sync
from celery import shared_task
from telegram import Bot

logger = logging.getLogger(__name__)

try:
    from db_saver import insert_to_db
    from rss_parser import rss_parser
except ModuleNotFoundError:
    sys.path.append(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from db_saver import insert_to_db
    from rss_parser import rss_parser


@shared_task
def parse_and_send_ads():
    """
    Задача для парсинга новых объявлений,
    их сохранения в базу и отправки пользователям.
    """
    try:
        # --- Парсинг новых объявлений ---
        logger.info("Начинается парсинг объявлений...")
        ads_pars = asyncio.run(rss_parser(httpx_client=httpx.AsyncClient()))
        # Сохранение объявлений в базу
        logger.info("Сохранение новых объявлений в базу данных...")
        new_ads = insert_to_db(ads_pars)
        if not new_ads:
            logger.info("Нет новых объявлений для сохранения.")
            return
        # --- Отправка новых объявлений ---
        logger.info("Отправка новых объявлений пользователям...")
        bot_token = os.environ.get("TELEGRAM_TOKEN")
        chat_id = os.environ.get("TELEGRAM_CHAT_ID")
        if not bot_token or not chat_id:
            raise ValueError(
                "Не задан TELEGRAM_TOKEN или TELEGRAM_CHAT_ID в переменных окружения.")
        bot = Bot(token=bot_token)
        for ad in new_ads:
            text = f"Новое объявление:\n\n*{ad['title']}*\n{ad['short_description']}\n[Подробнее]({ad['full_url']})"
            async_to_sync(
                bot.send_message)(
                    chat_id=chat_id, text=text, parse_mode="Markdown")
        logger.info(f"Успешно отправлено новых объявлений: {len(new_ads)}")
    except Exception as e:
        logger.error(f"Ошибка в процессе парсинга и отправки объявлений: {e}")
