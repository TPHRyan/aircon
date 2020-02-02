import math
from typing import ByteString, NewType


Checksum = NewType('Checksum', int)


def checksum(encoded_signal: ByteString) -> Checksum:
    checksum_val = 0
    for byte in encoded_signal:
        if byte >= 16:
            checksum_val += math.floor(byte / 16)
            byte = byte % 16
        checksum_val += byte

    return Checksum(checksum_val % 16)
