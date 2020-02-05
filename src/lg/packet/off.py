from lg.packet.raw import RawCommandPacket


class OffCommandPacket(RawCommandPacket):
    def __init__(self):
        super().__init__()
        self.length: int = 3
        self.data = 0b100010001100000000000101
