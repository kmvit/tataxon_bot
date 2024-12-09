import asyncio
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Optional

import django
import httpx
from django.db import DatabaseError
from django.db.models import Max

try:
    from api.models import Advertisement, Category
except django.core.exceptions.ImproperlyConfigured:
    # Запуск Django в не самого проекта
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tataxon_bot.settings')
    django.setup()
    from api.models import Advertisement, Category

try:
    from rss_parser import rss_parser
except ModuleNotFoundError:
    # Добавляем путь к родительскому каталогу в sys.path
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    )
    from rss_parser import rss_parser


LOGGING_FORMAT = (
    '%(asctime)s - %(levelname)s - %(funcName)s - %(lineno)d - %(message)s'
)

DATE_FORMAT = '%a, %d %b %y %H:%M:%S %z'

handler = logging.StreamHandler(
    stream=sys.stdout
)
formatter = logging.Formatter(
    LOGGING_FORMAT
)
handler.setFormatter(formatter)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


def safe_convert_to_category(category_title: str):
    """
    Получаем категорию, если она существует.
    Или создаём новую, если её нет.
    """
    category, _ = (Category.objects
                   .get_or_create(
                       title=category_title))
    return category


def safe_parse_datetime(date_str: str) -> Optional[datetime]:
    """
    Преобразуем формат RFC 822 в datetime объект
    К примеру Mon, 23 Sep 24 22:45:20 +0500в станет:
    datetime(
        2024,
        9,
        23,
        22,
        45,
        20,
        tzinfo=datetime.timezone(datetime.timedelta(seconds=18000))).
    """
    try:
        parsed_date = datetime.strptime(date_str, "%a, %d %b %y %H:%M:%S %z")
        return parsed_date.astimezone(timezone.utc)  # Преобразуем в UTC
    except ValueError:
        logger.error(f"'{date_str}' - не соответствует ожидаемому формату")
    except TypeError:
        logger.error(f"'{date_str}' - пустая строка")
    return None


def validation_of_new_advertisement(date_of_new_ad: datetime) -> bool:
    """
    Сравниваются самая поздняя дата объявления из базы данных с
    датой распарсенного объявления.
    """
    max_time_of_ad_in_db = Advertisement.objects.aggregate(
        Max('pub_date'))['pub_date__max']
    # Если в базе данных нет записей, считаем,
    # что дата нового объявления всегда валидна
    if max_time_of_ad_in_db is None:
        return True
      
    return max_time_of_ad_in_db < date_of_new_ad


def insert_to_db(data: list[dict[str]]) -> list[dict[str]]:
    """
    Преобразуем распарсенные данные в подходящие для БД,
    и делаем INSERT.
    """
    prepared_data = []
    new_ads = []
    for advertisement in data:
        advertisement_item = {
            'title': advertisement.get('title', ''),
            'short_description': advertisement.get('description', ''),
            'full_url': advertisement.get('link', ''),
            'pub_date': safe_parse_datetime(advertisement.get('pubDate', '')),
            'category': safe_convert_to_category(
                advertisement.get('category', ''))
        }
        if (
            advertisement_item['pub_date'] is not None
            and validation_of_new_advertisement(advertisement_item['pub_date'])
        ):
            prepared_data.append(Advertisement(**advertisement_item))
            new_ads.append(advertisement_item)
    try:
        Advertisement.objects.bulk_create(prepared_data)
    except DatabaseError as e:
        logger.error(f'Ошибка БД: {e}')
    return new_ads


if __name__ == '__main__':
    httpx_client = httpx.AsyncClient()
    data = asyncio.run(rss_parser(httpx_client))
    insert_to_db(data)
