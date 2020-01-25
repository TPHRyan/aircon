import enum
from abc import ABC
from command.tocode import ToCode
from typing import Union


class PacketComponent(ToCode, ABC):
    pass


class Speed(PacketComponent):
    def __init__(self, value: Union[int, str]):
        self.speed: SpeedValue
        try:
            self.speed = SpeedValue(self.convert_to_int(value))
        except ValueError:
            self.speed = SpeedValue(0)

    @property
    def value(self) -> int:
        return self.speed.value


class SpeedValue(enum.Enum):
    value: int

    DEHUM = 0b0000
    LOW = 0b0001
    MED = 0b0010
    UNKNOWN_0011 = 0b0011
    HIGH = 0b0100
    AUTO = 0b0101
    UNKNOWN_0110 = 0b0110
    UNKNOWN_0111 = 0b0111
    UNKNOWN_1000 = 0b1000
    UNKNOWN_1001 = 0b1001
    UNKNOWN_1010 = 0b1010
    UNKNOWN_1011 = 0b1011
    UNKNOWN_1100 = 0b1100
    UNKNOWN_1101 = 0b1101
    UNKNOWN_1110 = 0b1110
    UNKNOWN_1111 = 0b1111


class Temperature(PacketComponent):
    MIN_TEMPERATURE = 16
    MAX_TEMPERATURE = 30

    def __init__(self, temperature: Union[int, str] = 24):
        self._temperature: int = 0
        if isinstance(temperature, str):
            self.value = temperature
        else:
            self.temperature = temperature

    @property
    def temperature(self) -> int:
        return self._temperature

    @temperature.setter
    def temperature(self, temperature: Union[int, str]) -> None:
        temperature = self.convert_to_int(temperature)
        min_t = self.MIN_TEMPERATURE
        max_t = self.MAX_TEMPERATURE
        if temperature < min_t:
            print(f'Temperature provided lower than {min_t} - setting to {min_t}')
            temperature = 16
        elif temperature > 30:
            print(f'Temperature provided higher than {max_t} - setting to {max_t}')
            temperature = 30
        self._temperature = temperature

    @property
    def value(self) -> int:
        return self.temperature - 15

    @value.setter
    def value(self, temp_val: Union[int, str]):
        temp_val = self.convert_to_int(temp_val)
        self.temperature = temp_val + 15
