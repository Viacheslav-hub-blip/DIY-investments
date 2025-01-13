# репозиторий  - самый низкйи уровень работы с базой
from abc import ABC, abstractmethod
from typing import Optional
from src.users_api.database.databse import session_factory
from sqlalchemy import insert, select, delete


class AbstractRepository(ABC):
    @abstractmethod
    def insert(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    def select_all(self):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None
    DTOObject = None

    def insert(self, data: dict) -> int:
        with session_factory() as session:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            id = session.execute(stmt)
            session.commit()
            return id

    def select_all(self) -> [DTOObject]:
        with session_factory() as session:
            query = select(self.model)
            res = session.execute(query)
            orm = res.scalars().all()
            result_dto = [self.DTOObject.model_validate(row, from_attributes=True) for row in orm]
            return result_dto

    def select_by_id(self, id) -> Optional[DTOObject]:
        with session_factory() as session:
            try:
                query = select(self.model).where(self.model.id == id)
                res = session.execute(query)
                orm = res.scalars().all()
                result_dto = [self.DTOObject.model_validate(row, from_attributes=True) for row in orm]
                return result_dto[0]
            except:
                return None

    def delete_by_id(self, id: int) -> dict:
        with session_factory() as session:
            session.execute(
                delete(self.model)
                    .where(self.model.id == id)
            )
            session.commit()
            return {"res": "delete"}
