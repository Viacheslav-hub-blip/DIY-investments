from src.users_api.repositories.User_repository import UserRepository
from src.users_api.services.UserService import UserService


def user_service():
    return UserService(UserRepository)
