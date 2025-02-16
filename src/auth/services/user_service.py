from typing import Optional, NoReturn

from sqlalchemy.ext.asyncio import AsyncSession

from ..maps import map__user_model__user_dto
from ..models.dto import UserDto, InsertUserDto
from ..repositories.user import UserRepository
from ..exceptions import UserNotFoundException, UserAlreadyExistsException
from ..managers.interfaces import SecurityManagerInterface
from ...models.db import Database


class UserService:
    def __init__(self, database: Database, security_manger: SecurityManagerInterface) -> None:
        self.database = database
        self.security_manager = security_manger

        self._session: Optional[AsyncSession] = None
        self.__user_repository: Optional[UserRepository] = None

    @property
    def user_repository(self) -> UserRepository:
        if not self.__user_repository:
            self.__user_repository = UserRepository(self._session)
        return self.__user_repository

    async def get_by_email(self, email):
        async with self.database.auto_session() as self._session:
            user = await self.user_repository.get_user_by_email(email)

            if not user:
                raise UserNotFoundException(f'User with {email} not found')

            return user

    async def insert(self, user: InsertUserDto) -> UserDto:
        async with self.database.auto_session() as self._session:
            await self.__validate_unique_user(user)

            user.password = self.security_manager.get_hash(user.password)
            user = await self.user_repository.create_user(user)

            return map__user_model__user_dto(user)

    async def __validate_unique_user(self, user: UserDto) -> None:
        if await self.user_repository.get_user_by_email(user.email):
            raise UserAlreadyExistsException(f'Email {user.email} уже занят другим пользователем')
