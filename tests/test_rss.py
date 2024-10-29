from unittest.mock import AsyncMock

import pytest

from rss_parser import rss_parser


@pytest.mark.asyncio
async def test_rss_parser_successful_parsing():
    """
    Тест корректности извлечения данных из валидного RSS-ответа.
    """
    mock_response = AsyncMock()
    mock_response.text = """
    <rss>
        <channel>
            <item>
                <title>Ad Title</title>
                <link>https://example.com/ad</link>
                <description>Ad description</description>
                <category>Ad Category</category>
                <guid>https://example.com/ad</guid>
                <pubDate>Tue, 01 Jan 2021 00:00:00 +0000</pubDate>
            </item>
        </channel>
    </rss>
    """

    httpx_client = AsyncMock()
    httpx_client.get.return_value = mock_response

    result = await rss_parser(httpx_client)

    assert len(result) == 1
    assert result[0]['title'] == "Ad Title"
    assert result[0]['link'] == "https://example.com/ad"
    assert result[0]['description'] == "Ad description"
    assert result[0]['category'] == "Ad Category"
    assert result[0]['guid'] == "https://example.com/ad"
    assert result[0]['pubDate'] == "Tue, 01 Jan 2021 00:00:00 +0000"


@pytest.mark.asyncio
async def test_rss_parser_empty_response():
    """
    Тест корректной обработки случая,
    когда RSS-лента не содержит элементов <item>.
    """
    mock_response = AsyncMock()
    mock_response.text = """
    <rss>
        <channel>
        </channel>
    </rss>
    """

    httpx_client = AsyncMock()
    httpx_client.get.return_value = mock_response

    result = await rss_parser(httpx_client)

    assert result == []


@pytest.mark.asyncio
async def test_rss_parser_multiple_ads():
    """
    Тест корректности обработки нескольких элементов <item>.
    :return:
    """
    mock_response = AsyncMock()
    mock_response.text = """
    <rss>
        <channel>
            <item>
                <title>Ad 1</title>
                <link>https://example.com/ad1</link>
                <description>Description 1</description>
                <category>Category 1</category>
                <guid>https://example.com/ad1</guid>
                <pubDate>Tue, 01 Jan 2021 00:00:00 +0000</pubDate>
            </item>
            <item>
                <title>Ad 2</title>
                <link>https://example.com/ad2</link>
                <description>Description 2</description>
                <category>Category 2</category>
                <guid>https://example.com/ad2</guid>
                <pubDate>Wed, 02 Jan 2021 00:00:00 +0000</pubDate>
            </item>
            <item>
                <title>Ad 3</title>
                <link>https://example.com/ad3</link>
                <description>Description 3</description>
                <category>Category 3</category>
                <guid>https://example.com/ad3</guid>
                <pubDate>Wed, 02 Jan 2021 00:00:00 +0000</pubDate>
            </item>
        </channel>
    </rss>
    """

    httpx_client = AsyncMock()
    httpx_client.get.return_value = mock_response

    result = await rss_parser(httpx_client)

    assert len(result) == 3
    assert result[0]['title'] == "Ad 3"
    assert result[1]['title'] == "Ad 2"
    assert result[2]['title'] == "Ad 1"
