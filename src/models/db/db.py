from typing import Optional
from contextlib import contextmanager

from loguru import logger
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, sessionmaker, scoped_session

from src.config import Config
from src.exceptions.exceptions import NoDatabaseException


class Database:
    def __init__(self, config: Config) -> None:
        self.config = config

        self.is_db_ok = True
        self.__url_connection: Optional[URL] = None
        self.__session_factory: Optional[scoped_session] = None

        try:
            self.create_engine()
        except Exception:
            self.is_db_ok = False

    @contextmanager
    def auto_session(self):
        if not self.is_db_ok:
            raise NoDatabaseException('Can`t connect to database')

        current_session: Session = self.__session_factory()
        try:
            yield current_session
        except Exception:
            logger.error(f'Session rollback because of exception')
            current_session.rollback()
            raise
        else:
            current_session.commit()
        finally:
            current_session.close()

    @property
    def url_connection(self) -> URL:
        if not self.__url_connection:
            self.__url_connection = URL.create(
                drivername=self.config.db.drivername,
                username=self.config.db.username,
                password=self.config.db.password,
                host=self.config.db.host,
                port=int(self.config.db.port),
                database=self.config.db.database
            )
        return self.__url_connection

    def create_engine(self) -> None:

        engine = create_engine(self.url_connection, echo=True)
        self.__session_factory: scoped_session = scoped_session(
            sessionmaker(
                bind=engine,
                autoflush=False,
                autocommit=False,
                class_=Session
            )
        )
