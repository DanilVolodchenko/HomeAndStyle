from pydantic import BaseModel, EmailStr

from .constants import UserRoles


class BaseUserDto(BaseModel):
    email: EmailStr


class UserDto(BaseUserDto):
    role: UserRoles
    send_email: bool


class InsertUserDto(UserDto):
    password: str


class VerifyUserDto(BaseUserDto):
    password: str
