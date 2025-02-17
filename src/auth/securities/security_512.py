from datetime import timedelta
from typing import Optional, Any

import jwt
from passlib.ifc import PasswordHash
from passlib.hash import pbkdf2_sha512

from .interfaces import SecurityInterface
from ...config import config


class Security512(SecurityInterface):

    def __init__(self) -> None:
        self.__hash: Optional[PasswordHash] = None

    @property
    def hash(self) -> PasswordHash:
        if not self.__hash:
            self.__hash = pbkdf2_sha512
        return self.__hash

    def get_hash(self, data: str | bytes) -> str:
        return self.hash.hash(data)

    def verify(self, data: str | bytes, hashed_data: str) -> bool:
        result = self.hash.verify(data, hashed_data)
        return result

    def create_token(self, data: dict[str, Any], expire: timedelta) -> str:
        data.update({'expire': expire})

        return jwt.encode(
            payload=data, key=config.security.secret_key, algorithm=config.security.algorithm
        )
