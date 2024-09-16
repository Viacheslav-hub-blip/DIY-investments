from sqlalchemy.orm import Mapped, mapped_column
from src.database.databse import Base, engine


class SyncOrm:
    @staticmethod
    def create_tables():
        Base.metadata.drop_all(engine)
        engine.echo = False
        Base.metadata.create_all(engine)


class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    liked_company: Mapped[str]


