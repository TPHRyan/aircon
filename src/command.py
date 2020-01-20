from checksum import checksum
from signal import Signal
from typing import Any, List, Union


class CommandPacket(object):
    def __init__(self, from_data: Union[List[Signal]]):
        self._from_signals(from_data)

    def _from_signals(self, signals: List[Signal]):
        self.has_introduce_signal = False
        self.has_separate_signal = False
        self.parse_log = ''
        signal_pairs = zip(signals[::2], signals[1::2])
        binary_representation = ''
        for pair in signal_pairs:
            if pair == (Signal.SEPARATE, Signal.INTRO):
                self.has_introduce_signal = True
                self.has_separate_signal = True
            elif pair == (Signal.LOW, Signal.LOW):
                binary_representation += '0'
            elif pair == (Signal.LOW, Signal.HIGH):
                binary_representation += '1'
            else:
                self.log('Encountered unknown pair:', pair)
        self.unknown_data = binary_representation[:-4]
        self.checksum = checksum(self.unknown_data)
        provided_checksum = int(binary_representation[-4:], 2)
        if self.checksum != provided_checksum:
            self.log('WARNING: Command checksum does not match data!')
            self.log(f'Expected: {provided_checksum}, Actual: {self.checksum}')

    def __str__(self) -> str:
        return self.binary()

    def binary(self) -> str:
        bin_str = ''
        if self.has_separate_signal:
            bin_str += 'S-'
        if self.has_introduce_signal:
            bin_str += 'I-'
        bin_str += self.unknown_data
        bin_str += f'{self.checksum:0>4b}'
        return bin_str

    def log(self, *messages: Any) -> None:
        message = ' '.join(str(message) for message in messages)
        self.parse_log += message + '\n'
