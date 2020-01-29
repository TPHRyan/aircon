from abc import abstractmethod, ABC
from checksum import checksum
from command.packet.component import Speed, Temperature
from command.binary import BinarySerializable
from signal import Signal
from typing import Any, Callable, List, Optional, Union


class CommandPacket(BinarySerializable, ABC):
    def __init__(self, from_data: Optional[Union[List[Signal]]] = None):
        super().__init__()
        self.parse_log = ''

        binary_representation = self.binary_from_signals(from_data)[4:]
        provided_checksum = self.to_int(binary_representation[-4:])

        self.parse_binary(binary_representation)
        if self.checksum != provided_checksum:
            self.log('WARNING: Command checksum does not match data!')
            self.log(f'Expected: {provided_checksum}, Actual: {self.checksum}')

    @staticmethod
    def binary_from_signals(signals: List[Signal], output: Callable = print) -> str:
        signal_pairs = zip(signals[::2], signals[1::2])
        binary_representation = ''
        for pair in signal_pairs:
            if pair == (Signal.SEPARATE, Signal.INTRO):
                binary_representation += 'S-I-'
            elif pair == (Signal.LOW, Signal.LOW):
                binary_representation += '0'
            elif pair == (Signal.LOW, Signal.HIGH):
                binary_representation += '1'
            else:
                output('Encountered unknown pair:', pair)
        return binary_representation

    def __str__(self) -> str:
        return self.binary

    @property
    def binary(self) -> str:
        return f'{self.get_binary_encoding()}{self.checksum:0>4b}'

    @property
    def checksum(self) -> int:
        return checksum(self.get_binary_encoding())

    @abstractmethod
    def get_binary_encoding(self) -> str:
        pass

    @abstractmethod
    def parse_binary(self, binary_representation: str):
        pass

    def log(self, *messages: Any) -> None:
        message = ' '.join(str(message) for message in messages)
        self.parse_log += message + '\n'


class ModeCommandPacket(CommandPacket):
    def __init__(self, *args, **kwargs):
        self.unknown_data = ''
        self.speed = None
        self.temperature = None
        super().__init__(*args, **kwargs)

    def parse_binary(self, binary_representation: str):
        self.unknown_data = binary_representation[:16]
        self.temperature = Temperature(binary_representation[16:20])
        self.speed = Speed(binary_representation[20:24])

    def get_binary_encoding(self) -> str:
        return f'{self.unknown_data}{self.temperature.binary}{self.speed.binary}'
