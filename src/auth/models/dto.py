from pydantic import BaseModel, EmailStr

from ..models.db.constants import UserRoles


class UserDto(BaseModel):
    email: EmailStr


class CreateUserDto(UserDto):
    password: str
    role: UserRoles = UserRoles.USER
    send_email: bool


class VerifyUserDto(UserDto):
    password: str
