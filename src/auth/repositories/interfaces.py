from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.db import UserModel


class UserRepositoryInterface:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_by_id(self, id: int) -> UserModel | None:
        stmt = (
            select(UserModel)
            .where(UserModel.id == id)
        )
        result = await self.async_session.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_email(self, email: EmailStr) -> UserModel | None:
        stmt = (
            select(UserModel)
            .where(UserModel.email == email)
        )
        result = await self.async_session.execute(stmt)

        return result.scalar_one_or_none()
