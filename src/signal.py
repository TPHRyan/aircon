import enum
from typing import Type, TypeVar

T = TypeVar('T', bound='Signal')


class Signal(enum.Enum):
    SEPARATE = 8428
    INTRO = 4210
    HIGH = 1590
    LOW = 520

    @classmethod
    def from_int(cls: Type[T], signal: int) -> T:
        if signal < HL_THRESHOLD:
            return cls.LOW
        elif signal < IH_THRESHOLD:
            return cls.HIGH
        elif signal < SI_THRESHOLD:
            return cls.INTRO
        else:
            return cls.SEPARATE


SI_THRESHOLD = Signal.INTRO.value + (Signal.SEPARATE.value - Signal.INTRO.value) / 2
IH_THRESHOLD = Signal.HIGH.value + (Signal.INTRO.value - Signal.HIGH.value) / 2
HL_THRESHOLD = Signal.LOW.value + (Signal.HIGH.value - Signal.LOW.value) / 2
