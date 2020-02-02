from abc import ABC, abstractmethod
from typing import Union


def bytes_to_int(in_bytes: bytes) -> int:
    return int(in_bytes.hex(), 16)


def int_to_bytes(in_int: int) -> bytes:
    return bytes.fromhex(pad_bytes(in_int))


def lshift_bytes(in_bytes: bytes, shift_by=1) -> bytes:
    return bytes.fromhex(
        pad_bytes(
            bytes_to_int(in_bytes) << shift_by
        )
    )


def rshift_bytes(in_bytes: bytes, shift_by=1) -> bytes:
    return bytes.fromhex(
        pad_bytes(
            bytes_to_int(in_bytes) >> shift_by
        )
    )


def pad_bytes(in_bytes: Union[bytes, int]) -> str:
    if hasattr(in_bytes, 'hex'):
        bytes_str = in_bytes.hex()
    else:
        bytes_str = f'{in_bytes:0>x}'
    if len(bytes_str) % 2 == 1:
        bytes_str = '0' + bytes_str
    return bytes_str


class BinarySerializable(ABC):
    @property
    @abstractmethod
    def binary(self) -> bytes:
        return bytes()

    @property
    def int(self):
        return int(self.binary, 2)
