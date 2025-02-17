from abc import ABC, abstractmethod
from typing import Any
from datetime import timedelta


class SecurityInterface(ABC):

    @abstractmethod
    def get_hash(self, data: str | bytes) -> str:
        """
        :param data: any string or bytes that be used to get hash;
        :return: hashed data.
        """

    @abstractmethod
    def verify(self, data: str | bytes, hashed_data: str) -> bool:
        """
        :param data: any string or bytes that be used to verify;
        :param hashed_data: hashed string that be compared with data;
        :return: True/False.
        """

    @abstractmethod
    def create_token(self, data: dict[str, Any], expires_time: timedelta) -> str:
        """
        :param data: data to create token;
        :param expires_time: expires token time;
        :return: created token.
        """
