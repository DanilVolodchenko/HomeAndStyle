from abc import ABC, abstractmethod


class SecurityManagerInterface(ABC):

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
        return self.__hash.verify(data, hashed_data)
