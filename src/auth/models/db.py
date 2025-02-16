from sqlalchemy import VARCHAR, BOOLEAN, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from .constants import UserRoles
from ...models.db import Base


class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(VARCHAR, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    role: Mapped[UserRoles] = mapped_column(default=UserRoles.USER)
    send_email: Mapped[bool] = mapped_column(BOOLEAN, default=True)
