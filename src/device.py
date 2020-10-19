import time

import broadlink
from typing import Generator, List


SUPPORTED_TYPES = ['RM2', 'RM4']


NO_SUPPORTED_DEVICES = RuntimeError('No supported devices found!')


def acquire_device() -> broadlink.rm:
    try:
        device = next(discover_devices_of_types(SUPPORTED_TYPES))
    except StopIteration:
        raise NO_SUPPORTED_DEVICES
    if not isinstance(device, broadlink.rm):
        raise NO_SUPPORTED_DEVICES
    print('Device found! Authenticating...')
    auth = device.auth()
    tries = 0
    while auth is None and tries < 3:
        print('Device not authenticated, retrying...')
        time.sleep(1)
        device.auth()
        tries += 1
    if tries >= 3:
        raise RuntimeError('Could not authenticate device!')
    return device


def discover_devices_of_types(types: List[str] = None) -> Generator[broadlink.device, None, None]:
    for device in broadlink.xdiscover():
        if device.type in types:
            yield device
