from typing import Annotated

from pydantic import EmailStr
from fastapi import APIRouter, Query, Depends
from dependency_injector.wiring import inject, Provide

from .models.dto import UserDto, InsertUserDto, VerifyUserDto, Token
from .container import AuthContainer
from .services.user_service import UserService
from .services.auth_service import AuthService

auth_router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


@auth_router.post('/register', response_model=UserDto)
@inject
async def register(
        user: InsertUserDto, user_service: UserService = Depends(Provide[AuthContainer.user_service])
) -> UserDto:
    return await user_service.insert(user)


@auth_router.post('/login', response_model=Token)
@inject
async def login(user: VerifyUserDto, auth_service: AuthService = Depends(Provide[AuthContainer.auth_service])) -> Token:
    verify_user = await auth_service.authenticate_user(user)
    return await auth_service.create_token(verify_user)


@auth_router.get('/user', response_model=UserDto)
@inject
async def get_by_email(
        email: Annotated[EmailStr, Query()], user_service: UserService = Depends(Provide[AuthContainer.user_service])
) -> UserDto:
    return await user_service.get_by_email(email)


@auth_router.delete('/user', response_model=UserDto | None)
@inject
async def delete(
        email: Annotated[EmailStr, Query()], user_service: UserService = Depends(Provide[AuthContainer.user_service])
) -> UserDto | None:
    return await user_service.delete(email)

# @auth_router.get('/user/me')
# @inject
# async def get_user(email: Annotated[EmailStr, Query()]):
#     from ..common.services.user import UserService
#     from ..models.db.db import Database
#     from ..config import config
#
#     user = UserService(Database(config))
#     return await user.get_user_by_email(email)
