from fastapi import APIRouter, Depends
from src.users_api.schemas.schemas import UserInsertDTO, UserLogin, TokenGetting, UpdateLikedCompany
from src.users_api.dependencies import user_service
from src.users_api.services.UserService import UserService
from typing import Annotated
from src.users_api.schemas.schemas import UserDTO
from src.users_api.auth import UserAuth

router = APIRouter(
    prefix="/users_api",
    tags=["Users"],
)
user_auth = UserAuth()


@router.post("/insert")
async def insert_user(user: UserInsertDTO,
                      user_service: Annotated[UserService, Depends(user_service)]
                      ):
    status = user_service.insert_user(user)
    return status


@router.get("")
async def get_users(user_service: Annotated[UserService, Depends(user_service)]):
    users = user_service.select_users()
    return users


@router.get("/user_by_id")
async def get_user_by_id(id: int,
                         user_service: Annotated[UserService, Depends(user_service)]
                         ):
    user = user_service.select_user_by_id(id)
    return user


@router.get("/user_by_email")
async def get_user_by_email(email: str,
                            user_service: Annotated[UserService, Depends(user_service)]
                            ) -> UserDTO:
    user = user_service.select_user_by_email(email)
    return user


@router.post("/update")
async def update_user_name(user_id: int, new_name: str, user_service: Annotated[UserService, Depends(user_service)]):
    res = user_service.update_user_name(user_id, new_name)
    return res


@router.post("/delete")
async def delete_user(user_id: int,
                      user_service: Annotated[UserService, Depends(user_service)]):
    res = user_service.delete_user(user_id)
    return res

@router.post('/add_company')
async def update_company(data: UpdateLikedCompany,
                         user_service: Annotated[UserService, Depends(user_service)]
                         ):
    print('добавление компании')
    return user_service.add_liked_company(data.user_id, data.company)


@router.post("/delete_company")
async def delete_company(data: UpdateLikedCompany,
                        user_service: Annotated[UserService, Depends(user_service)]
                         ):
    print('удаление')
    return user_service.delete_liked_company(data.user_id, data.company)


@router.post("/login")
async def login(user: UserLogin):
    token = user_auth.login_for_access_token(user.email, user.password)
    return token


@router.post("/me")
async def read_users_me(token: TokenGetting):
    print('me', user_auth.get_current_user(token.token))
    return user_auth.get_current_user(token.token)
