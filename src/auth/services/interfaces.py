from abc import ABC
from typing import Callable

from passlib.utils.handlers import GenericHandler


class SecurityServiceInterface(ABC):

    def __init__(self, hash_handler) -> None:
        self.__hash = hash_handler

    def hash(self, data: str | bytes) -> str:
        """
        :param data: any string or bytes that be used to get hash;
        :return: hashed data.
        """
        return self.__hash.hash(data)

    def verify(self, data: str | bytes, hashed_data: str) -> bool:
        """
        :param data: any string or bytes that be used to verify;
        :param hashed_data: hashed string that be compared with data;
        :return: True, if data is correct, False in another case.
        """
        return self.__hash.verify(data, hashed_data)
