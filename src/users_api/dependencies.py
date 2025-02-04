from src.users_api.repositories.user_repository import UserRepository
from src.users_api.services.user_service import UserService


def user_service():
    return UserService(UserRepository)
