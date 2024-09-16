from typing import Optional
from sqlalchemy import select, update
from src.database.databse import session_factory
from src.users_api.repositories.base_rep import SQLAlchemyRepository
from src.users_api.models.models import UserORM
from src.users_api.schemas.schemas import UserDTO


class UserRepository(SQLAlchemyRepository):
    model = UserORM
    DTOObject = UserDTO

    def select_user_by_email(self, email: str) -> Optional[DTOObject]:
        with session_factory() as session:
            try:
                query = select(self.model).where(self.model.email == email)
                res = session.execute(query)
                user_orm = res.scalars()
                user_dto = [self.DTOObject.model_validate(row, from_attributes=True) for row in user_orm]
                return user_dto[0]
            except:
                return None

    def update_user_name(self, user_id: int, new_username: str) -> dict:
        with session_factory() as session:
            session.execute(
                update(self.model).
                    where(self.model.id == user_id)
                    .values({"login": new_username})
            )
            session.commit()
            return {"new name": new_username}

    def delete_liked_company(self, user_id: int, company: str):
        try:
            with session_factory() as session:
                user = self.select_by_id(user_id)
                new_liked_company = (user.liked_company).replace(company, '')
                print(new_liked_company)
                session.execute(
                    update(self.model).where(self.model.id == user_id)
                        .values({'liked_company': new_liked_company})
                )
                session.commit()
                return {"status": f"удалено {company}"}
        except:
            return {"status": f"ошибка удаления"}

    def update_liked_companies(self, user_id: int, new_company: str) -> dict:
        try:
            with session_factory() as session:
                user = self.select_by_id(user_id)
                if new_company not in user.liked_company.split(' '):
                    new_liked_company = user.liked_company + ' ' + new_company
                    session.execute(
                        update(self.model).where(self.model.id == user_id)
                            .values({'liked_company': new_liked_company})
                    )
                    session.commit()
                    return {"status": f"добалено {new_company}"}
        except Exception:
            return {"status": f"ошибка добаления"}
