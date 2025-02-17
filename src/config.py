from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from src import __version__
from src.constants import EnvironmentEnum


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore', env_file='.env.dev', env_file_encoding='utf-8')


class LocalServer(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='LOCAL_')

    api_prefix: str = '/api/v1'
    host: str
    port: int
    environment: EnvironmentEnum = EnvironmentEnum.PRODUCTION


class Allows(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='ALLOW_')

    origins: list[str] = ['http://localhost', 'http://localhost:8080', 'http://localhost:8081']
    credentials: bool = True
    methods: list[str] = ['*']
    headers: list[str] = ['*']


class DB(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='DB_')

    drivername: str = 'postgresql+asyncpg'
    username: str
    password: str
    host: str
    port: str
    database: str = 'homeandstyle'


class Security(BaseConfig):
    model_config = SettingsConfigDict()

    secret_key: str
    algorithm: str
    access_token_expire_minutes: int


class Log(BaseConfig):
    model_config = SettingsConfigDict(env_prefix='LOG_')

    level: int = 3
    retention_days: int = 7


class Config(BaseSettings):
    local_server: LocalServer = Field(default_factory=LocalServer)
    db: DB = Field(default_factory=DB)
    allows: Allows = Field(default_factory=Allows)
    security: Security = Field(default_factory=Security)
    log: Log = Field(default_factory=Log)


config = Config()
app_config: dict[str, Any] = {'title': 'Home&Style', 'version': __version__, 'prefix': config.local_server.api_prefix}

if not config.local_server.environment.is_debug:
    app_config['openapi_url'] = None
