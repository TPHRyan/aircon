import math
import re
from typing import Iterable, List

from command import RawCommandPacket
from signal import Signal


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


def string_from_signals(in_signals: Iterable[Signal]) -> str:
    output: str = ''
    for signal in in_signals:
        signal_val: int = round(signal.value / 8192 * 269)
        values: List[int] = []
        while signal_val > 256:
            output += '00'
            values.append(math.floor(signal_val / 256))
            signal_val %= 256
        values.append(signal_val)
        for value in values:
            output += f'{value:0>2x}'
    return output


BYTES_PATTERN = re.compile(r'[0-9a-f]{2}')


def decode_packet(packet: str) -> RawCommandPacket:
    input_bytes: List[str] = list(map(''.join, zip(packet[0::2], packet[1::2])))
    if input_bytes[0] != '26':
        raise RuntimeError('Cannot decode file: packet is not an IR packet!')
    if input_bytes[1] != '00':
        raise NotImplementedError('Cannot decode repeated packets yet!')
    packet_length = int(f'{int(input_bytes[3], 16):0>2x}{int(input_bytes[2], 16):0>2x}', 16)
    remaining_bytes: List[str] = input_bytes[4:]
    signal_string: str = ''
    while packet_length > 0:
        next_byte, remaining_bytes = remaining_bytes[0], remaining_bytes[1:]
        signal_string += next_byte
        packet_length -= 1
    if signal_string[-4:] != '0d05':
        raise RuntimeError('Invalid packet: end marker not found!')

    return RawCommandPacket(signals_from_string(signal_string[:-4]))


def decode_file(file_path: str) -> RawCommandPacket:
    input_bytes: str = ''
    with open(file_path) as f:
        for line in f:
            comment_start = line.find('//')
            if comment_start >= 0:
                line = line[:comment_start]
            for byte_match in BYTES_PATTERN.finditer(line.lower().strip()):
                byte_pattern = byte_match.group(0)
                input_bytes += byte_pattern
    return decode_packet(input_bytes)


def encode_packet(packet: Iterable[Signal]) -> bytes:
    payload = string_from_signals(packet)
    # Pad if leading 0 is missing
    if len(payload) % 2 == 1:
        payload = '0' + payload

    if len(payload) % 4 == 2:
        # Add another 00 to even out the packet length(?)
        payload += '00'

    # Add the end marker
    payload += '0d05'
    payload_size = len(payload) / 2
    payload_size_hi, payload_size_lo = divmod(payload_size, 256)
    return bytes.fromhex(
        '26'                                                        # IR packet
        '00'                                                        # No repeats
        f'{int(payload_size_lo):0>2x}{int(payload_size_hi):0>2x}'   # Little-endian length
        f'{payload}'
    )
