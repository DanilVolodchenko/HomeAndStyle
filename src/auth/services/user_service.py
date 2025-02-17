from typing import Optional

from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession

from ..maps import map__user_model__user_dto
from ..models.dto import UserDto, InsertUserDto
from ..repositories.user_interface import UserRepository
from ..exceptions import UserNotFoundException, UserAlreadyExistsException
from ..securities.interfaces import SecurityInterface
from ...models.db import Database


class UserService:
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

    async def get_by_email(self, email: EmailStr) -> UserDto:
        async with self.database.auto_session() as self._session:
            user = await self.user_repository.get_by_email(email)

            if not user:
                raise UserNotFoundException(f'Пользователь с email={email} не найден')

            return map__user_model__user_dto(user)

    async def get_by_id(self, id: int) -> UserDto:
        async with self.database.auto_session() as self._session:
            user = await self.user_repository.get_by_id(id)

            if not user:
                raise UserNotFoundException(f'Пользователь с id={id} не найден')

            return map__user_model__user_dto(user)

    async def insert(self, user: InsertUserDto) -> UserDto:
        async with self.database.auto_session() as self._session:
            await self.__validate_unique_user(user)

            user.password = self.security.get_hash(user.password)
            inserted_user = await self.user_repository.insert(user.model_dump(exclude_none=True))

            return map__user_model__user_dto(inserted_user)

    async def update(self, user: ):

    async def delete(self, email: EmailStr) -> UserDto | None:
        async with self.database.auto_session() as self._session:
            deleted_user = await self.user_repository.delete(email)

            return map__user_model__user_dto(deleted_user) if deleted_user else None

    async def __validate_unique_user(self, user: UserDto) -> None:
        if await self.user_repository.get_by_email(user.email):
            raise UserAlreadyExistsException(f'Email {user.email} уже занят другим пользователем')
