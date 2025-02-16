from typing import Optional, AsyncIterator
from contextlib import asynccontextmanager
from asyncio import current_task

from loguru import logger
from sqlalchemy import URL, text
from sqlalchemy.ext.asyncio import async_sessionmaker, async_scoped_session, create_async_engine, AsyncSession, \
    AsyncEngine

from src.common.exceptions.exceptions import NoDatabaseException
from ...config import config


class Database:
    def __init__(self) -> None:
        self.__url_connection: Optional[URL] = None
        self.__session_factory: Optional[async_scoped_session[AsyncSession]] = None
        self.__engine: Optional[AsyncEngine] = None

        self.is_db_ok: bool = True
        try:
            self.create_async_engine()
        except Exception as exc:
            logger.error('Database connection error: {}'.format(exc))
            self.is_db_ok = False

    @asynccontextmanager
    async def auto_session(self) -> AsyncIterator[AsyncSession]:
        if not self.is_db_ok:
            raise NoDatabaseException('Can`t connect to database')

        current_session: AsyncSession = self.__session_factory()
        try:
            yield current_session
        except Exception:
            logger.error(f'Session rollback because of exception')
            await current_session.rollback()
            raise
        else:
            await current_session.commit()
        finally:
            await current_session.close()

    @property
    def url_connection(self) -> URL:
        if not self.__url_connection:
            self.__url_connection = URL.create(
                drivername=config.db.drivername,
                username=config.db.username,
                password=config.db.password,
                host=config.db.host,
                port=int(config.db.port),
                database=config.db.database
            )
        return self.__url_connection

    def create_async_engine(self) -> None:
        self.__engine = create_async_engine(self.url_connection, echo=True, pool_pre_ping=True)

        self.__session_factory: async_scoped_session = async_scoped_session(
            async_sessionmaker(
                bind=self.__engine,
                autoflush=False,
                autocommit=False,
                class_=AsyncSession
            ),
            scopefunc=current_task
        )

    async def check_connection(self) -> bool:
        try:
            async with self.__engine.connect() as connect:
                await connect.execute(text('SELECT 1'))
            self.is_db_ok = True
            return True
        except Exception as exc:
            logger.error("Database connection check failed: {}", exc)
            self.is_db_ok = False
            return False
