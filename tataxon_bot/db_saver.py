import os
import httpx
import asyncio
from datetime import datetime

import django
from django.db import DatabaseError

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
    import sys
    # Добавляем путь к родительскому каталогу в sys.path
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__)))
    )
    from rss_parser import rss_parser


DATE_FORMAT = '%a, %d %b %y %H:%M:%S %z'


def safe_convert_to_category(category_title: str):
    """
    Получаем категорию, если она существует.
    Или создаём новую, если её нет.
    """
    category, _ = (Category.objects
                   .get_or_create(
                       title=category_title
                   ))
    return category


def safe_parse_datetime(date_str: str) -> datetime | None:
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
        return datetime.strptime(date_str, DATE_FORMAT)
    except ValueError:
        print(f'{date_str} - не соответствует ожидаемому формату')
    except TypeError:
        print(f'{date_str} - пустая строка')
    except AttributeError:
        print(f'{date_str} - ошибка с временной зоной')
    return ''


def insert_to_db(data: list[dict[str]]) -> None:
    """
    Преобразуем распарсенные данные в подходящие для БД,
    и делаем INSERT.
    """
    prepared_data = []
    for advertisement in data:
        advertisement_item = {}
        advertisement_item['title'] = advertisement.get('title', '')
        advertisement_item['short_description'] = advertisement.get(
            'description', ''
        )
        advertisement_item['full_url'] = advertisement.get('link', '')
        advertisement_item['pud_date'] = safe_parse_datetime(
            advertisement.get('pubDate', '')
        )
        advertisement_item['category'] = safe_convert_to_category(
            advertisement.get('category', '')
        )
        prepared_data.append(Advertisement(**advertisement_item))
    try:
        Advertisement.objects.bulk_create(prepared_data)
    except DatabaseError:
        print('Ошибка БД.')


if __name__ == '__main__':
    httpx_client = httpx.AsyncClient()
    data = asyncio.run(rss_parser(httpx_client))
    insert_to_db(data)
