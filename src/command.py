from checksum import checksum
from signal import Signal
from typing import Any, List, Union


class CommandPacket(object):
    def __init__(self, from_data: Union[List[Signal]]):
        self._from_signals(from_data)

    def _from_signals(self, signals: List[Signal]):
        self.parse_log = ''
        signal_pairs = zip(signals[::2], signals[1::2])
        binary_representation = ''
        for pair in signal_pairs:
            if pair[0] == Signal.SEPARATE:
                binary_representation += 'S-I-'
            elif pair[0] == Signal.LOW and pair[1] == Signal.LOW:
                binary_representation += '0'
            elif pair[0] == Signal.LOW and pair[1] == Signal.HIGH:
                binary_representation += '1'
            else:
                self.log('Encountered unknown pair:', pair)
        self.unknown_data = binary_representation[4:-4]
        self.checksum = binary_representation[-4:]
        if checksum(self.unknown_data) != self.checksum:
            self.log('WARNING: Command checksum does not match data!')

    def __str__(self) -> str:
        return self.binary()

    def binary(self) -> str:
        return 'S-I-' + self.unknown_data + self.checksum

    def log(self, *messages: Any) -> None:
        message = ' '.join(str(message) for message in messages)
        self.parse_log += message + '\n'
