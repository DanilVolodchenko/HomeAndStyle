from typing import Annotated

from fastapi import APIRouter

from src.auth.dto import UserDto, CreateUserDto, VerifyUserDto

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@auth_router.post('/register', response_model=UserDto)
async def register(user: CreateUserDto):
    return UserDto(email=user.email)


@auth_router.post('/login')
async def login(user: VerifyUserDto): # TODO сдесь скорее всего можно сделать через зависимости: проверять пароль и логин пользователя
    pass

