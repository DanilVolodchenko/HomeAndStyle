from typing import Self
from pydantic import BaseModel, EmailStr, model_validator

from .constants import UserRoles
from ..exceptions import PasswordException


class BaseUserDto(BaseModel):
    id: int | None = None
    email: EmailStr


class UserDto(BaseUserDto):
    role: UserRoles
    send_email: bool | None = None


class InsertUserDto(UserDto):
    password: str

class UpdateUserDto(UserDto):
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def check_passwords(self) -> Self:
        if self.password != self.confirm_password:
            raise PasswordException('Пароли не совпадают')
        return self

class VerifyUserDto(BaseUserDto):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
