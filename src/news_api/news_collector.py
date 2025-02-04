import asyncio
import time
from repositories.news_repository import NewsRepository
from services.news_api_service import NewsApiService, NewsCard

news_repository = NewsRepository()


async def collect_news_and_insert_in_db(query, from_date) -> None:
    news_service = NewsApiService(api_key='6b67f68055a5498d8c15661fd747b201')
    news = await news_service.get_news(query, from_date)
    news_cards = await news_service.convert_news_to_card_news(query, news)
    print('собранные новости за', from_date, 'о', query)
    for news_card in news_cards:
        print(news_card)
    await news_repository.insert_unique_news(news_cards, query)


async def main():
    companies = [
        'Amazon',
        'Tesla',
        'Nvidia',
        'Facebook'
    ]

    tasks = []

    while True:
        from_date = '2025-01-30'
        for company in companies:
            tasks.append(asyncio.create_task(collect_news_and_insert_in_db(company, from_date)))

        for task in tasks:
            await task
        print('задержка')
        time.sleep(180)


if __name__ == '__main__':
    print(time.strftime('%X'))

    asyncio.run(main())
    print(time.strftime('%X'))
