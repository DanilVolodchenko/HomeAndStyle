from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.user import UserRepository
from ..exceptions import UserNotFoundException
from ...models.db import Database


class UserService:
    def __init__(self, database: Database) -> None:
        self.database = database

        self._session: Optional[AsyncSession] = None
        self.__user_repository: Optional[UserRepository] = None

    @property
    def user_repository(self) -> UserRepository:
        if not self.__user_repository:
            self.__user_repository = UserRepository(self._session)
        return self.__user_repository

    async def get_user_by_email(self, email):
        async with self.database.auto_session() as self._session:
            user = await self.user_repository.get_user_by_email(email)
            if not user:
                raise UserNotFoundException(f'User with {email} not found')
            return user

    async def create_user(self, user: C):