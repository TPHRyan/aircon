import math
from typing import ByteString, Iterable, Iterator, List

from ir.signal import Signal

END_MARKER = (0x0d, 0x05)


def broadlink_signal_packet_to_ir(bytes_in: Iterable[int]) -> Iterator[Signal]:
    bytes_in = list(bytes_in)
    bytes_iter = iter(bytes_in)
    try:
        byte_val = next(bytes_iter)
        if byte_val == END_MARKER[0] and next(bytes_iter) == END_MARKER[1]:
            return
        elif byte_val == 0:
            hi_val, lo_val = next(bytes_iter), next(bytes_iter)
            if (hi_val, lo_val) == END_MARKER:
                return
            signal_val = hi_val * 256 + lo_val
        else:
            signal_val = byte_val
        yield Signal.from_int(round(signal_val / 269 * 8192))
        yield from broadlink_signal_packet_to_ir(bytes_iter)
    except StopIteration:
        raise RuntimeError('Invalid packet: end marker not found!')


def broadlink_full_packet_to_ir(*, bytes_in: ByteString) -> Iterator[Signal]:
    if bytes_in[0] != 0x26:
        raise RuntimeError('Cannot decode file: packet is not an IR packet!')
    if bytes_in[1] != 0x00:
        raise NotImplementedError('Cannot decode repeated packets yet!')
    packet_length: int = int(
        bytes(reversed(bytes_in[2:4])).hex(),  # [2:4:-1] doesn't work.
        16
    )
    remaining_bytes: ByteString = bytes_in[4:]
    signal_bytes: bytearray = bytearray(remaining_bytes[:packet_length])
    return broadlink_signal_packet_to_ir(signal_bytes)


def ir_to_broadlink_signal_packet(*, signals_in: Iterable[Signal]) -> bytearray:
    output: bytearray = bytearray(0)
    for signal in signals_in:
        signal_val: int = round(signal.value / 8192 * 269)
        while signal_val > 256:
            output.append(0)
            output.append(math.floor(signal_val / 256))
            signal_val %= 256
        output.append(signal_val)
    return output


def ir_to_broadlink_full_packet(*, signals_in: Iterable[Signal]) -> bytearray:
    payload = ir_to_broadlink_signal_packet(signals_in=signals_in)
    if len(payload) % 2 == 1:
        # Add another 00 to even out the packet length(?)
        payload.append(0)

    # Add the end marker
    payload.extend(END_MARKER)
    payload_size = len(payload)
    payload_size_hi, payload_size_lo = divmod(payload_size, 256)
    full_packet = bytearray([
        0x26,
        0x00,
        payload_size_lo,
        payload_size_hi,
    ])
    full_packet.extend(payload)
    return full_packet
