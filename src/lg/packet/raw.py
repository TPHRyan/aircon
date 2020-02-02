from typing import Iterable

import binary
from lg.packet import LGCommandPacket


class RawCommandPacket(LGCommandPacket):
    def __init__(self, *args, **kwargs):
        self._data: str = ''
        self.length: int = 0
        super().__init__(*args, **kwargs)

    def __len__(self):
        return self.length

    def __getitem__(self, item) -> str:
        if not isinstance(int, item):
            raise ValueError(
                'Index provided should be the place value of the bit you want to get!'
            )
        return self._data[-item - 1]

    def __setitem__(self, key, value):
        msb = self.length - 1
        if not isinstance(int, key):
            raise ValueError(
                'Index provided should be the place value of the bit you want to set!'
            )
        if key > msb:
            raise ValueError(f'Cannot set bit {key}, MSB is {msb}!')
        self._data = self._data[:-key - 1] + str(value) + self._data[-key:]

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data: str):
        if len(data) > self.length:
            raise ValueError(
                'Cannot mutate packet value to a size greater than original value!'
            )
        self._data = f'{data:0>{self.length}b}'

    def parse_bytes(self, byte_iter: Iterable[int]):
        _data = ''
        for byte in byte_iter:
            _data += f'{byte:0>8b}'
        self._data = _data
        self.length = len(_data)

    def get_binary_encoding(self) -> bytes:
        return binary.int_to_bytes(int(self.data, 2))
