from typing import Any

from pydantic import EmailStr
from sqlalchemy import insert, delete

from .interfaces import UserRepositoryInterface
from ..models.db import UserModel


class UserRepository(UserRepositoryInterface):

    async def insert(self, user: dict[str, Any]) -> UserModel:
        stmt = (
            insert(UserModel)
            .values(user)
            .returning(UserModel)
        )
        result = await self.async_session.execute(stmt)

        return result.scalar_one()

    async def delete(self, email: EmailStr) -> UserModel | None:
        stmt = (
            delete(UserModel)
            .where(UserModel.email == email)
            .returning(UserModel)
        )
        result = await self.async_session.execute(stmt)

        return result.scalar_one_or_none()
