import asyncio

from src.news_api.database.connection import engine, get_db, SessionLocal
from src.news_api.database.create_tables import News
from src.news_api.services.news_api_service import NewsCard
from sqlalchemy import select, insert
from src.news_api.dto_objects.schemas import NewsDTO


class NewsRepository:
    async def insert_news(self, news: [NewsCard]):
        print('-----------------------Добавление----------------------')
        print(len(news))
        async with SessionLocal() as session:
            for news in news:
                await session.execute(
                    insert(News).values(
                        company=news.company,
                        title=news.title,
                        description=news.description,
                        url=news.url,
                        img_url=news.img_url,
                        published_at=news.published_at,
                    )
                )
            await session.commit()

    async def select_news_by_company(self, company: str, limit=None) -> list[NewsDTO]:
        async with SessionLocal() as session:
            # noinspection PyTypeChecker
            result = (
                await session.execute(
                    select(News)
                    .filter(News.company == company)
                    .order_by(News.published_at.desc())
                )
            ).scalars().all()

            if limit is not None:
                result = result[:limit]
                return [NewsDTO.model_validate(row, from_attributes=True) for row in result]
            else:
                return [NewsDTO.model_validate(row, from_attributes=True) for row in result]

    async def insert_unique_news(self, all_news: [NewsCard], query: str):
        news_in_base = await self.select_news_by_company(query)
        news_in_base_titles = [news.title for news in news_in_base]
        news_out_base = []

        for news in all_news:
            if news.title not in news_in_base_titles:
                news_out_base.append(NewsCard(
                    company=news.company,
                    title=news.title,
                    description=news.description,
                    url=news.url,
                    img_url=news.img_url,
                    published_at=news.published_at,
                ))
        print(len(news_out_base), 'новости вне базы', news_out_base)
        await self.insert_news(news_out_base)


if __name__ == '__main__':
    async def main():
        news_repository = NewsRepository()

        result = await news_repository.select_news_by_company('Tesla')
        for res in result:
            print(res)


    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())
