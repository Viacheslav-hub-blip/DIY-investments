import asyncio
from sqlalchemy import Table, Column, Integer, String, MetaData
from src.news_api.database.connection import Base
from src.news_api.database.connection import engine

# from src.news_api.database.connection import engine

#
# metadata = MetaData()
#
# news_table = Table(
#     'news', metadata,
#     Column('id', Integer, primary_key=True),
#     Column('company', String),
#     Column('title', String),
#     Column('description', String),
#     Column('url', String),
#     Column('img_url', String),
#     Column('published_at', String)
# )
#
#
# async def init_models():
#     async with engine.begin() as conn:
#         await conn.run_sync(metadata.create_all)
#
# asyncio.run(init_models())

class News(Base):
    __tablename__ = 'news'

    id = Column(Integer, primary_key=True)
    company = Column(String)
    title = Column(String)
    description = Column(String)
    url = Column(String)
    img_url = Column(String)
    published_at = Column(String)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(init_models())
