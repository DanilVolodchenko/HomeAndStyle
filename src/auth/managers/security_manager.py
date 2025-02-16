from typing import Optional

from passlib.ifc import PasswordHash
from passlib.hash import pbkdf2_sha512

from .interfaces import SecurityManagerInterface


class Security512Manager(SecurityManagerInterface):

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
        return self.hash.verify(data, hashed_data)
