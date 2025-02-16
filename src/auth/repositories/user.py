from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from ..models.db import UserModel
from ..models.dto import InsertUserDto


class UserRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_user_by_email(self, email: EmailStr) -> Optional[UserModel]:
        stmt = (
            select(UserModel)
            .where(UserModel.email == email)
        )
        result = await self.async_session.execute(stmt)

        return result.scalar_one_or_none()

    async def create_user(self, user: InsertUserDto) -> UserModel:
        stmt = (
            insert(UserModel)
            .values(user.model_dump())
            .returning(UserModel)
        )
        result = await self.async_session.execute(stmt)

        return result.scalar_one()
