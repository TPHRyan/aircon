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

        self.parse_binary(binary_representation[:-4])
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


class RawCommandPacket(CommandPacket):
    def __init__(self, *args, **kwargs):
        self._data: str = ''
        self.length: int = 0
        super().__init__(*args, **kwargs)

    def __len__(self):
        return self.length

    def __getitem__(self, item) -> str:
        if not isinstance(int, item):
            raise ValueError(
                'Index provided should be the place value of the bit you want to get!'
            )
        return self._data[-item - 1]

    def __setitem__(self, key, value):
        msb = self.length - 1
        if not isinstance(int, key):
            raise ValueError(
                'Index provided should be the place value of the bit you want to set!'
            )
        if key > msb:
            raise ValueError(f'Cannot set bit {key}, MSB is {msb}!')
        self._data = self._data[:-key - 1] + str(value) + self._data[-key:]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: str):
        if len(data) > self.length:
            raise ValueError(
                'Cannot mutate packet value to a size greater than original value!'
            )
        self._data = f'{data:0>{self.length}b}'

    def parse_binary(self, binary_representation: str):
        self._data = binary_representation
        self.length = len(binary_representation)

    def get_binary_encoding(self) -> str:
        return self.data


class ModeCommandPacket(CommandPacket):
    def __init__(self, *args, **kwargs):
        self.unknown_data: str = ''
        self.speed = None
        self.temperature = None
        super().__init__(*args, **kwargs)

    def parse_binary(self, binary_representation: str):
        self.unknown_data = binary_representation[:16]
        self.temperature = Temperature(binary_representation[16:20])
        self.speed = Speed(binary_representation[20:24])

    def get_binary_encoding(self) -> str:
        return f'{self.unknown_data}{self.temperature.binary}{self.speed.binary}'
