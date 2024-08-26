from src.users_api.repositories.base_rep import AbstractRepository
from src.users_api.schemas.schemas import UserInsertDTO, UserDTO


class UserService:
    def __init__(self, user_repo: AbstractRepository):
        self.user_repo = user_repo()

    def insert_user(self, user: UserInsertDTO):
        user_dict = user.model_dump()
        user_id = self.user_repo.insert_user(user_dict)
        return user_id

    def select_users(self) -> UserDTO:
        users = self.user_repo.select_all()
        return users

    def select_user_by_id(self, user_id: int):
        user = self.user_repo.select_user_by_id(user_id)
        return user

    def update_user_name(self, user_id: int, new_name: str):
        res = self.user_repo.update_user_name(user_id, new_name)
        return res

    def select_user_by_email(self, email:str):
        user  = self.user_repo.select_user_by_email(email)
        return user

    def delete_user(self, user_id: int):
        res = self.user_repo.delete_by_id(user_id)
        return res

    def update_liked_company(self, user_id: int, new_company: str):
        res = self.user_repo.update_liked_companies(user_id, new_company)
        return res

    def validate_user_password(self, email: str, password: str) -> bool:
        try:
            user = self.user_repo.select_user_by_email(email)
            if user.password.__eq__(password):
                return True
            else:
                return False
        except:
            return False
