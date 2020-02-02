import enum
from typing import Union, Iterator

from lg.packet import ParsedCommandPacket, LGPacketError
from packet import PacketComponent


class ModeCommandPacket(ParsedCommandPacket):
    def __init__(self, *args, **kwargs):
        self.mode: ModeValue = ModeValue.ON
        self.speed: SpeedValue = SpeedValue.LOW
        self.temperature: Temperature = Temperature()
        super().__init__(*args, **kwargs)

    def consume_bytes(self, byte_iter: Iterator[int]):
        super().consume_bytes(byte_iter)
        try:
            command_byte = next(byte_iter)
            payload_byte = next(byte_iter)
        except StopIteration:
            raise LGPacketError('Insufficient data to create Mode command!')
        if command_byte & 0xf0 != 0:
            raise LGPacketError('Command byte should be 0x0X!')
        try:
            self.mode = ModeValue(command_byte & 0x0f)
            self.speed = SpeedValue(payload_byte & 0xf0)
            self.temperature = Temperature(payload_byte & 0x0f)
        except ValueError as e:
            raise LGPacketError(str(e))

    def get_binary_encoding(self) -> bytes:
        encoding = bytearray(super().get_binary_encoding())
        encoding.append(self.mode.value)
        encoding.append(self.speed.value)
        encoding.extend(self.temperature.binary)
        return encoding


class ModeValue(enum.Enum):
    value: int

    ON = 0b0000
    COOL = 0b1000
    DEHUMIDIFY = 0b1001
    AUTO = 0b1011
    HEAT = 0b1100


class SpeedValue(enum.Enum):
    value: int

    DEHUM = 0b0000
    LOW = 0b0001
    MED = 0b0010
    HIGH = 0b0100
    CHAOS = 0b0101


class Temperature(PacketComponent):
    MIN_TEMPERATURE = 16
    MAX_TEMPERATURE = 30

    def __init__(self, temperature: Union[bytes, int] = 9):
        self._temperature: bytes = bytes([1])
        self.temperature = temperature

    @property
    def temperature(self) -> bytes:
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: Union[int, bytes]) -> None:
        if isinstance(temperature, bytes):
            self._temperature: bytes = temperature
        else:
            self._temperature: bytes = bytes([temperature])

    @property
    def temperature_degrees(self) -> int:
        return self.temperature[0] + 15

    @temperature_degrees.setter
    def temperature_degrees(self, temperature: int):
        min_t = self.MIN_TEMPERATURE
        max_t = self.MAX_TEMPERATURE
        if temperature < min_t:
            print(f'Temperature provided lower than {min_t} - setting to {min_t}')
            temperature = 16
        elif temperature > 30:
            print(f'Temperature provided higher than {max_t} - setting to {max_t}')
            temperature = 30
        self.temperature = temperature - 15

    @property
    def binary(self) -> bytes:
        return self.temperature
