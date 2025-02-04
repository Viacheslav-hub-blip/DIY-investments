import asyncio
from aiohttp import ClientSession
from typing import NamedTuple


class NewsCard(NamedTuple):
    company: str
    title: str
    description: str
    url: str
    img_url: str
    published_at: str


class NewsApiService:
    def __init__(self, api_key: str):
        self.api_key: str = api_key
        self.url: str = "https://newsapi.org/v2/top-headlines?q={query}&from={from_date}&apiKey={api_key}"

    async def get_news(self, query: str, from_date: str) -> dict:
        async with ClientSession() as session:
            async with session.get(self.url.format(query=query, from_date=from_date, api_key=self.api_key)) as response:
                news: dict = await response.json()
        return news['articles']

    async def convert_news_to_card_news(self, query, all_news: dict) -> list[NewsCard]:
        news_cards: list[NewsCard] = []
        for news in all_news:
            card = NewsCard(query, news['title'], news['description'], news['url'], news['urlToImage'],
                            news['publishedAt'])
            news_cards.append(card)
        return news_cards


if __name__ == '__main__':
    async def main():
        query = 'Amazon'
        news_service = NewsApiService(api_key='6b67f68055a5498d8c15661fd747b201')
        news = await news_service.get_news(query, '2024-12-29')
        news_cards = await news_service.convert_news_to_card_news(query, news)
        for card in news_cards:
            print(card)


    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
