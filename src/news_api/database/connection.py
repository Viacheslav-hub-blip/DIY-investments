from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_USER = 'postgres'
DB_PASSWORD = '123'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'finance_platform_db'

db_url = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"

engine = create_async_engine(db_url)
SessionLocal = async_sessionmaker(bind=engine)
session = SessionLocal()
Base = declarative_base()


async def get_db() -> SessionLocal:
    async with SessionLocal() as session:
        yield session
# connection = engine.connect()
# print('connection', connection)
