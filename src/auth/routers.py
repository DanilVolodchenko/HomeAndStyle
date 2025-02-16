from typing import Annotated

from fastapi import APIRouter, Query, Depends
from dependency_injector.wiring import inject, Provide

from .models.dto import UserDto, InsertUserDto, VerifyUserDto
from .container import AuthContainer
from .services.user_service import UserService

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@auth_router.post('/register', response_model=UserDto)
@inject
async def register(user: InsertUserDto, user_service: UserService = Depends(Provide[AuthContainer.user_service])):
    return await user_service.insert(user)


@auth_router.post('/login')
@inject
async def login(
        user: VerifyUserDto):  # TODO сдесь скорее всего можно сделать через зависимости: проверять пароль и логин пользователя
    pass


# @auth_router.get('/user/me')
# @inject
# async def get_user(email: Annotated[EmailStr, Query()]):
#     from ..common.services.user import UserService
#     from ..models.db.db import Database
#     from ..config import config
#
#     user = UserService(Database(config))
#     return await user.get_user_by_email(email)
