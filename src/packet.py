from abc import ABC, abstractmethod
from typing import Callable, Iterable, Optional, Any

from binary import BinarySerializable
from ir.signal import Signal

DecoderFunction = Callable[[Iterable[Signal]], bytes]


class BasePacket(BinarySerializable, ABC):
    def __init__(
            self,
            from_data: Optional[Iterable[Signal]] = None,
            *args,
            **kwargs
    ):
        self.parse_log: str = ''
        if from_data is not None:
            self.parse_bytes(self.decode_ir(from_data))

    @abstractmethod
    def decode_ir(self, signals: Iterable[Signal]) -> Iterable[int]:
        pass

    @property
    @abstractmethod
    def binary(self) -> bytes:
        pass

    @abstractmethod
    def parse_bytes(self, byte_iter: Iterable[int]):
        pass

    @property
    @abstractmethod
    def encode_ir(self) -> Iterable[Signal]:
        pass

    def log(self, *messages: Any) -> None:
        message = ' '.join(str(message) for message in messages)
        self.parse_log += message + '\n'


class PacketComponent(BinarySerializable, ABC):
    pass
