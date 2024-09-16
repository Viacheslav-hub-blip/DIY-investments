from typing import Union, NamedTuple

from fastapi import HTTPException, status

from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from src.config import settings
from src.users_api.repositories.User_repository import UserRepository
from src.users_api.schemas.schemas import UserDTO, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
user_repository = UserRepository()

bearer_payload_email: str = "useremail"
bearer_payload_password: str = "password"
bearer_payload_exp: str = "exp"
#
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

class UserAuth:

    def validate_user(self, email: str, password: str) -> Union[UserDTO, bool]:
        '''
        Проверка наличия пользователя и пароля
        :param email: email пользовтеля
        :param password: пароль пользователя
        :return: возвращаем данные пользователя, если сущесвует в базе, либо False
        '''
        user: UserDTO = user_repository.select_user_by_email(email)
        if user and user.password.__eq__(password):
            return user
        else:
            return False

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        '''
        Создание Bearer токена
        :param data: данные для кодирования в токен
        :param expires_delta: время действия токена
        :return: возвращаем токен
        '''
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({bearer_payload_exp: expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def login_for_access_token(self, email: str, password: str) -> Token:
        '''
        Вход пользователя. Если пользователь существует, возвращаем токен
        :param email: email пользовтеля
        :param password: пароль пользователя
        :return: возвращает токен
        '''
        user: UserDTO = self.validate_user(email, password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={bearer_payload_email: user.email, bearer_payload_password: user.password},
            expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer", access_token_expires=str(access_token_expires))

    def get_current_user(self, token: str):
        """
        Данные пользователя по токену
        :param token: bearer токен
        :return: данные пользовтеля или ошибка
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            # декодировка токена
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            #данные из токена
            email: str = payload.get(bearer_payload_email)
            password: str = payload.get(bearer_payload_password)
            exp: str = payload.get(bearer_payload_exp)

            if email is None:
                raise credentials_exception

            if datetime.fromtimestamp(float(exp)) - datetime.now() < timedelta(0):
                raise credentials_exception

        except InvalidTokenError:
            raise credentials_exception

        #проверка данных
        user: UserDTO = self.validate_user(email, password)

        if user is None:
            raise credentials_exception
        return user
