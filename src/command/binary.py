from abc import abstractmethod, ABC
from typing import Union


class BinarySerializable(ABC):
    @staticmethod
    def to_int(int_or_binary_string: Union[int, str]) -> int:
        if isinstance(int_or_binary_string, str):
            return int(int_or_binary_string, 2)
        else:
            return int_or_binary_string

    @staticmethod
    def to_binary(int_or_binary_string: Union[int, str], pad_length: int = 0) -> str:
        if isinstance(int_or_binary_string, str):
            return int_or_binary_string
        else:
            return f'{int_or_binary_string:0>{pad_length}b}'

    @property
    @abstractmethod
    def binary(self) -> str:
        return ''

    @property
    def int(self):
        return int(self.binary, 2)
