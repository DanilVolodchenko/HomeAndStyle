from dependency_injector import containers, providers

from .securities.security_512 import Security512
from .services.user_service import UserService
from .services.auth_service import AuthService
from ..models.db.db import Database


class AuthContainer(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=['.routers'])

    database = providers.Singleton(Database)

    security_512 = providers.Factory(Security512)

    user_service = providers.Factory(UserService, database, security_512)
    auth_service = providers.Factory(AuthService, database, security_512)
