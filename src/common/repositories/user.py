from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import EmailStr

from ...models.db.user import User


class UserRepository:
    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def get_user_by_email(self, email: EmailStr) -> User:
        stmt = select(User).where(User.email == email)
        return await self.async_session.scalar(stmt)
