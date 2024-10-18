import asyncio
from bs4 import BeautifulSoup
import httpx

from api.models import Advertisement

ERROR_DOM_TREE = (
    'Ошибка {error} при представлении XML-кода RSS-ленты {url} '
    'в виде дерева объектов'
)
RSS_LINK_TAXATON = (
    'https://tataxon.uz/rss.php?content=ads&title=TATAXON.uz'
)

httpx_client = httpx.AsyncClient()


async def rss_parser(httpx_client):
    """ Функция парсит rss ленту и добавляет объявления в базу. """
    error_messages = []
    try:
        response = await httpx_client.get(RSS_LINK_TAXATON)
    except ConnectionError as error:
        error_messages.append(
            ERROR_DOM_TREE.format(error=error, url=RSS_LINK_TAXATON)
        )
        await asyncio.sleep(15)

    soup = BeautifulSoup(response.text, features='xml')

    all_ads = soup.find_all('item')

    Advertisement.objects.abulk_create(
        Advertisement(
            title=ad.find('title').text,
            short_description=ad.find('description').text,
            image=ad.find('image').text if ad.find('image') else None,
            full_url=ad.find('link').text,
            category=ad.find('category').text,
            pud_date=ad.find('pubDate').text,
        ) for ad in all_ads
    )
