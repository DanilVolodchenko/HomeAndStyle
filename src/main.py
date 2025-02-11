import asyncio

import uvicorn
from uvicorn import Config, Server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.config import config, app_config
from src.auth import auth_router


def create_app() -> FastAPI:
    app = FastAPI(**app_config)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.allows.origins,
        allow_credentials=config.allows.credentials,
        allow_methods=config.allows.methods,
        allow_headers=config.allows.headers,
    )

    app.include_router(auth_router)

    return app


def run() -> None:
    app = create_app()

    uvicorn_config = Config(
        app=app,
        host=config.local_server.host,
        port=config.local_server.port
    )

    uvicorn.run(app, host=config.local_server.host, port=config.local_server.port)


if __name__ == '__main__':
    run()