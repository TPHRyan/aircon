from command import CommandPacket
import re
from signal import Signal
from typing import List


def signals_from_string(in_str: str) -> List[Signal]:
    in_str = in_str.strip()
    if len(in_str) % 2 == 1:
        in_str = '0' + in_str
    output: List[Signal] = []
    byte_val = 0
    bytes_left = 1
    for byte in map(''.join, zip(in_str[::2], in_str[1::2])):
        if bytes_left == 0:
            output.append(Signal.from_int(round(byte_val / 269 * 8192)))
            byte_val = 0
            bytes_left = 1
        if byte == '00':
            bytes_left += 1
        else:
            byte_val += int(byte, 16) * 256 ** (bytes_left - 1)
            bytes_left -= 1
    return output


COMMENT_PATTERN = re.compile(r'^[^/]*//[^/]*$')


def decode_file(file_path: str) -> CommandPacket:
    signals: List[Signal] = []
    with open(file_path) as f:
        for line in f:
            if not COMMENT_PATTERN.match(line):
                if line.strip() == '':
                    continue
                signals += signals_from_string(line)
    return CommandPacket(signals)

