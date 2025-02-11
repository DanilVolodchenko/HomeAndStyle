from dependency_injector import containers, providers
from passlib.hash import pbkdf2_sha512

from src.auth.services.security_service import Security512Service


class AuthContainer(containers.DeclarativeContainer):
    security_512_service = providers.Factory(Security512Service, pbkdf2_sha512)
    r = security_512_service.provided
    print(r)


from dependency_injector.wiring import Provide, inject


@inject
def main(sec_ser: Security512Service = Provide[AuthContainer.security_512_service]):
    return sec_ser.hash('12')


if __name__ == 'AuthContainer':
    container = AuthContainer()
    container.wire(modules=[__name__])

    print(main())
