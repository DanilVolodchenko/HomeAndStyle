from dependency_injector import providers, containers

from ..auth.container import AuthContainer


class CommonContainer(containers.DeclarativeContainer):
    auth_container = providers.Container(AuthContainer)
