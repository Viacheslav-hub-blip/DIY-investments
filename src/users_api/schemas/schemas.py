from typing import Union

from pydantic import BaseModel


class UserInsertDTO(BaseModel):
    login: str
    email: str
    password: str

class UserLogin(BaseModel):
    email:str
    password:str


class UserDTO(BaseModel):
    id: int
    login: str
    email: str
    password: str
    liked_company: str

class TokenGetting(BaseModel):
    token:str

class Token(BaseModel):
    access_token: str
    token_type: str
    access_token_expires: str


class TokenData(BaseModel):
    email: Union[str, None] = None
    password: Union[str, None] = None

class UpdateLikedCompany(BaseModel):
    user_id: int
    company: str
