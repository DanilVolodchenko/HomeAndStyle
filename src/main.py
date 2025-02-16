from uvicorn import Config, Server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from .auth import auth_router
from .config import config, app_config
from .common.container import CommonContainer
from .common.exceptions.exception_handlers import validation_error_handler, internal_exception, home_and_style_exception
from .common.exceptions.exceptions import HomeAndStyleBaseException


def create_app() -> FastAPI:
    common_container = CommonContainer()
    app = FastAPI(**app_config)

    app.container = common_container

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allows.origins,
        allow_credentials=config.allows.credentials,
        allow_methods=config.allows.methods,
        allow_headers=config.allows.headers,
    )

    app.add_exception_handler(Exception, internal_exception)
    app.add_exception_handler(ValidationError, validation_error_handler)
    app.add_exception_handler(HomeAndStyleBaseException, home_and_style_exception)

    app.include_router(auth_router)

    return app


async def run() -> None:
    app = create_app()

    uvicorn_config = Config(
        app=app,
        host=config.local_server.host,
        port=config.local_server.port
    )

    await Server(uvicorn_config).serve()
