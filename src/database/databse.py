from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
from sqlalchemy import create_engine
from src.config import settings


class Base(DeclarativeBase):
    pass


engine = create_engine(
    url=settings.DATABSE_URL_psycopg
)

session_factory = sessionmaker(engine)
print('session', session_factory)


def get_session():
    with session_factory() as session:
        return session
