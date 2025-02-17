from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..maps import map__user_model__user_dto
from ..models.dto import UserDto, Token, VerifyUserDto
from ..repositories.user_interface import UserRepository
from ..exceptions import UserNotFoundException
from ..securities.interfaces import SecurityInterface
from ...models.db import Database
from ...config import config


class AuthService:
    def __init__(self, database: Database, security: SecurityInterface) -> None:
        self.database = database
        self.security = security

        self._session: Optional[AsyncSession] = None
        self.__user_repository: Optional[UserRepository] = None

    @property
    def user_repository(self) -> UserRepository:
        if not self.__user_repository:
            self.__user_repository = UserRepository(self._session)
        return self.__user_repository

    async def authenticate_user(self, user: VerifyUserDto) -> UserDto:
        async with self.database.auto_session() as self._session:
            current_user = await self.user_repository.get_by_email(user.email)

            if not user or not self.security.verify(user.password, current_user.password):
                raise UserNotFoundException('Неверный логин или пароль')

            return map__user_model__user_dto(current_user)

    async def create_token(self, user: UserDto) -> Token:
        token = self.security.create_token(user.model_dump(), config.security.access_token_expire_minutes)

        return Token(access_token=token, token_type='JWT')
