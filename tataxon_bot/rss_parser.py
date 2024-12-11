import asyncio

import httpx
from bs4 import BeautifulSoup
from httpx import ConnectTimeout

ERROR_DOM_TREE = (
    'Ошибка {error} при представлении XML-кода RSS-ленты {url} '
    'в виде дерева объектов'
)
RSS_LINK_TAXATON = (
    'https://tataxon.uz/rss.php?content=ads&title=TATAXON.uz'
)


async def rss_parser(httpx_client):
    '''Парсер rss ленты'''

    error_messages = []
    try:
        response = await httpx_client.get(RSS_LINK_TAXATON)
    except ConnectionError as error:
        error_messages.append(
            ERROR_DOM_TREE.format(error=error, url=RSS_LINK_TAXATON)
        )
    except ConnectTimeout as error:
        error_messages.append(
            f'Ошибка при подключении: {error}'
        )
        await asyncio.sleep(15)

    soup = BeautifulSoup(response.text, features='xml')

    all_ads = soup.find_all('item')
    list_of_ads = []
    for ad in all_ads[::-1]:
        # формируется объявление
        ad_in_base = dict(
            title=ad.find('title').text,
            link=ad.find('link').text,
            description=ad.find('description').text,
            category=ad.find('category').text,
            guid=ad.find('guid').text,
            pubDate=ad.find('pubDate').text,
        )
        list_of_ads.append(ad_in_base)
    return list_of_ads


if __name__ == "__main__":

    httpx_client = httpx.AsyncClient()

    asyncio.run(rss_parser(httpx_client))
