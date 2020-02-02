from abc import ABC, abstractmethod
from typing import Generator, Iterable, Iterator, List

import binary
import lg.checksum
from ir.signal import Signal
from packet import BasePacket


class LGPacketError(ValueError):
    def __init__(self, message: str, *args, **kwargs):
        super().__init__('Invalid LG packet: ' + message, *args)


class LGCommandPacket(BasePacket, ABC):
    def __str__(self) -> str:
        return f'{binary.bytes_to_int(self.binary):0>28b}'

    def decode_ir(self, signals: Iterable[Signal]) -> Iterable[int]:
        signals: List[Signal] = list(signals)
        signal_pairs = zip(signals[::2], signals[1::2])
        if next(signal_pairs) != (Signal.SEPARATE, Signal.INTRO):
            raise LGPacketError('Separate + Introduce not given!')

        lg_bytes = bytes([0])
        for pair in signal_pairs:
            if pair == (Signal.LOW, Signal.LOW):
                this_bit = 0
            elif pair == (Signal.LOW, Signal.HIGH):
                this_bit = 1
            else:
                self.log(f'Encountered unknown pair: {pair}')
                continue
            shifted_val = f'{(int(lg_bytes.hex(), 16) << 1) + this_bit:0>x}'
            if len(shifted_val) % 2 == 1:
                shifted_val = '0' + shifted_val
            lg_bytes = bytes.fromhex(shifted_val)
        provided_checksum = lg.checksum.Checksum(lg_bytes[-1] & 0b00001111)

        no_checksum_bytes = bytearray(lg_bytes[:-1])
        no_checksum_bytes.append(lg_bytes[-1] & 0b11110000)
        lg_bytes = binary.rshift_bytes(no_checksum_bytes, 4)
        if lg.checksum.checksum(lg_bytes) != provided_checksum:
            self.log(
                'WARNING: Command checksum does not match data!\n'
                f'Expected: {provided_checksum}, Actual: {lg.checksum.checksum}'
            )
        return lg_bytes

    @property
    def binary(self) -> bytes:
        binary_encoding = int(self.get_binary_encoding().hex(), 16) << 4
        return binary.int_to_bytes(binary_encoding + self.checksum)

    @abstractmethod
    def get_binary_encoding(self) -> bytes:
        pass

    @property
    def encode_ir(self) -> Generator[Signal, None, None]:
        binary_str = str(self)
        yield Signal.SEPARATE
        yield Signal.INTRO
        for bit in binary_str:
            yield Signal.LOW
            yield Signal.HIGH if bit == '1' else Signal.LOW
        # Ensure we finish with a LOW signal(?)
        yield Signal.LOW

    @property
    def checksum(self) -> lg.checksum.Checksum:
        return lg.checksum.checksum(self.get_binary_encoding())


class ParsedCommandPacket(LGCommandPacket, ABC):
    def get_binary_encoding(self) -> bytes:
        return bytes([0x80, 0x80])

    def parse_bytes(self, byte_iter: Iterable[int]):
        self.consume_bytes(iter(byte_iter))

    @abstractmethod
    def consume_bytes(self, byte_iter: Iterator[int]):
        first_byte = next(byte_iter)
        if first_byte != 0x88:
            raise LGPacketError('First byte should be 0x88!')
