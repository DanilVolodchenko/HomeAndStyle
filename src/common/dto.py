from pydantic import BaseModel, EmailStr


class UserDto(BaseModel):
    email: EmailStr


class CreateUserDto(UserDto):
    password: str


class VerifyUserDto(UserDto):
    password: str
