import re

import ir.decoder
from lg.packet.raw import RawCommandPacket

BYTES_PATTERN = re.compile(r'[0-9a-f]{2}')


def decode_file(file_path: str) -> RawCommandPacket:
    input_bytes: bytearray = bytearray()
    with open(file_path) as f:
        for line in f:
            comment_start = line.find('//')
            if comment_start >= 0:
                line = line[:comment_start]
            for byte_match in BYTES_PATTERN.finditer(line.lower().strip()):
                byte_pattern = byte_match.group(0)
                input_bytes.append(int(byte_pattern, 16))
    return RawCommandPacket(
        ir.decoder.broadlink_full_packet_to_ir(bytes_in=input_bytes)
    )
