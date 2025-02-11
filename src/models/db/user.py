from sqlalchemy import VARCHAR, BOOLEAN, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from src.models.db.base import Base
from src.models.db.constants import UserRoles


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(INTEGER, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(VARCHAR, nullable=False, unique=True)
    password: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    role: Mapped[UserRoles] = mapped_column(default=UserRoles.USER)
    send_email: Mapped[bool] = mapped_column(BOOLEAN, default=True)
