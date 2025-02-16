from dependency_injector import containers, providers
from passlib.hash import pbkdf2_sha512

from .managers.security_manager import Security512Manager
from .services.user_service import UserService
from ..models.db.db import Database


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['.routers'])

    database = providers.Singleton(Database)

    security_512_manager = providers.Factory(Security512Manager)

    user_service = providers.Factory(UserService, database, security_512_manager)
