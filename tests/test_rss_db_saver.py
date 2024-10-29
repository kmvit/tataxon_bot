from unittest.mock import AsyncMock

import pytest
from asgiref.sync import sync_to_async

from api.models import Advertisement, Category
from db_saver import (insert_to_db, safe_convert_to_category,
                      safe_parse_datetime)
from rss_parser import rss_parser


@pytest.mark.django_db
def test_safe_convert_to_category_existing():
    """
    Функция возвращает существующую категорию, если она уже есть в базе данных.
    """
    category = Category.objects.create(title="Test Category")
    result = safe_convert_to_category("Test Category")
    assert result == category


@pytest.mark.django_db
def test_safe_convert_to_category_new():
    """
    Функция создает новую категорию, если её нет.
    """
    result = safe_convert_to_category("New Category")
    assert result.title == "New Category"


@pytest.mark.parametrize("date_str, expected_year, expected_month", [
    ("Mon, 23 Sep 24 22:45:20 +0000", 2024, 9),
    ("Tue, 01 Jan 21 00:00:00 +0000", 2021, 1),
])
def test_safe_parse_datetime_valid(date_str, expected_year, expected_month):
    """
    Функция правильно преобразует корректные строки в объекты datetime.
    """
    result = safe_parse_datetime(date_str)
    assert result.year == expected_year
    assert result.month == expected_month


@pytest.mark.parametrize("date_str", [
    "Invalid Date",
    "Not a Date",
    "Another Invalid Format",
    "",
    None
])
def test_safe_parse_datetime_invalid_format(date_str):
    """
    Функция обрабатывает некорректные строки, возвращая None.
    """
    result = safe_parse_datetime(date_str)
    assert result is None


@pytest.mark.django_db
def test_insert_to_db_success():
    """
    Функция корректно добавляет объявления в базу данных, если данные валидные.
    """
    data = [
        {
            "title": "Ad 1",
            "description": "Description 1",
            "link": "https://example.com/ad1",
            "pubDate": "Mon, 23 Sep 24 22:45:20 +0000",
            "category": "Test Category",
        }
    ]
    insert_to_db(data)
    assert Advertisement.objects.count() == 1


@pytest.mark.django_db
def test_insert_to_db_invalid_date():
    """
    Функция обрабатывает случаи, когда невалидные данные не добавляются.
    """
    data = [
        {
            "title": "Ad 2",
            "description": "Description 2",
            "link": "https://example.com/ad2",
            "pubDate": "Invalid Date",
            "category": "Test Category",
        }
    ]
    insert_to_db(data)
    assert Advertisement.objects.count() == 0


@pytest.mark.asyncio
@pytest.mark.django_db
async def test_full_flow():
    """
    Тест получения данных из парсера, их обработку и вставку в базу данных.
    """
    mock_response = AsyncMock()
    mock_response.text = """
    <rss>
        <channel>
            <item>
                <title>Ad 1</title>
                <link>https://example.com/ad1</link>
                <description>Description 1</description>
                <category>Test Category</category>
                <guid>https://example.com/ad1</guid>
                <pubDate>Mon, 23 Sep 24 22:45:20 +0000</pubDate>
            </item>
        </channel>
    </rss>
    """

    httpx_client = AsyncMock()
    httpx_client.get.return_value = mock_response

    data = await rss_parser(httpx_client)
    await sync_to_async(insert_to_db)(data)
    ad_count = await sync_to_async(Advertisement.objects.count)()
    assert ad_count == 1
