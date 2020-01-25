from abc import abstractmethod, ABC
from typing import Union


class ToCode(ABC):
    @staticmethod
    def convert_to_int(int_or_binary_string: Union[int, str]):
        if isinstance(int_or_binary_string, str):
            return int(int_or_binary_string, 2)
        else:
            return int_or_binary_string

    @property
    def binary(self) -> str:
        return f'{self.value:0>4b}'

    @property
    @abstractmethod
    def value(self) -> int:
        return 0
