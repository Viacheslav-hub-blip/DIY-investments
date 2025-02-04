import asyncio

from src.news_api.repositories.news_repository import NewsRepository, NewsDTO
from src.news_api.services.news_api_service import NewsCard


class NewsController:
    def __init__(self):
        self.news_repository = NewsRepository()

    async def _convert_news_dto_to_dict(self, all_news: list[NewsDTO]) -> list[dict]:
        news_cards = []
        for news in all_news:
            card = news.model_dump()
            news_cards.append(card)
        return news_cards

    async def get_news_by_query_from_db(self, query: str) -> list[dict]:
        news = await self.news_repository.select_news_by_company(query)
        news = await self._convert_news_dto_to_dict(news)
        return news


if __name__ == '__main__':

    async def main():
        controller = NewsController()
        news = await controller.get_news_by_query_from_db('Amazon')
        print('результат')
        for new in news:
            print(new)


    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
