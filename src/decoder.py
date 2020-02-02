import re

import ir.decoder
from lg.packet.raw import LGCommandPacket

BYTES_PATTERN = re.compile(r'[0-9a-f]{2}')


def decode_file(file_path: str) -> LGCommandPacket:
    input_bytes: bytearray = bytearray()
    with open(file_path) as f:
        for line in f:
            comment_start = line.find('//')
            if comment_start >= 0:
                line = line[:comment_start]
            for byte_match in BYTES_PATTERN.finditer(line.lower().strip()):
                byte_pattern = byte_match.group(0)
                input_bytes.append(int(byte_pattern, 16))
    return LGCommandPacket.create(
        ir.decoder.broadlink_full_packet_to_ir(bytes_in=input_bytes)
    )
