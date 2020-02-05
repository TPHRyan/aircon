from typing import Iterable, Union

import binary
from lg.packet import LGCommandPacket


class RawCommandPacket(LGCommandPacket):
    def __init__(self, *args, **kwargs):
        self._data: bytearray = bytearray()
        self.length: int = 0
        super().__init__(*args, **kwargs)

    def __len__(self):
        return self.length

    def __getitem__(self, item) -> int:
        if not isinstance(int, item):
            raise ValueError(
                'Index provided should be the place value of the bit you want to get!'
            )
        byte_index, bit_place = divmod(item, 8)
        return 1 if self._data[byte_index] & (2 ** bit_place) else 0

    def __setitem__(self, key, value):
        msb = self.length - 1
        if not isinstance(int, key):
            raise ValueError(
                'Index provided should be the place value of the bit you want to set!'
            )
        if key > msb:
            raise ValueError(f'Cannot set bit {key}, MSB is {msb}!')
        byte_index, bit_place = divmod(key, 8)
        self._data[byte_index] = self._data[byte_index] | (2 ** bit_place)

    @property
    def data(self) -> bytes:
        return bytes(self._data)

    @data.setter
    def data(self, data: Union[bytes, int, str]):
        if isinstance(data, str):
            if not data.isdigit():
                raise ValueError('If string is provided, it must be a binary sequence.')
            if len(data) > self.length * 8:
                raise ValueError(
                    'Cannot mutate packet value to a size greater than original value!'
                )
            data_str = data
            data_bytes = bytearray()
            while len(data_str) > 0:
                data_bytes.append(int(data_str[-8:], 2))
                data_str = data_str[:-8]
        elif isinstance(data, int):
            if data > 2 ** (self.length * 8):
                raise ValueError(
                    'Cannot mutate packet value to a size greater than original value!'
                )
            data_bytes = bytearray(binary.int_to_bytes(data))
        else:
            if len(data) > self.length:
                raise ValueError(
                    'Cannot mutate packet value to a size greater than original value!'
                )
            data_bytes = bytearray(data)
        self._data = data_bytes

    def parse_bytes(self, byte_iter: Iterable[int]):
        _data = bytearray()
        for byte in byte_iter:
            _data.append(byte)
        self._data = _data
        self.length = len(_data) * 8

    def get_binary_encoding(self) -> bytes:
        return self.data
