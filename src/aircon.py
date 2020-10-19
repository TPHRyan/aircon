import os

import decoder
import ir.decoder
from lg.packet import LGCommandPacket, OffCommandPacket
from lg.packet.mode import ModeCommandPacket, ModeValue, SpeedValue

from device import acquire_device

ALLOWED_MODES = {
    'on': ModeValue.ON,
    'auto': ModeValue.AUTO,
    'cool': ModeValue.COOL,
    'dehumidify': ModeValue.DEHUMIDIFY,
    'heat': ModeValue.HEAT,
}

ALLOWED_SPEEDS = {
    'chaos': SpeedValue.CHAOS,
    'low': SpeedValue.LOW,
    'med': SpeedValue.MED,
    'high': SpeedValue.HIGH,
}


def custom_command():
    command: LGCommandPacket
    command_in = input('Command to run? ')
    if command_in == 'mode':
        mode_in = input('What mode to select? ')
        try:
            mode_value = ALLOWED_MODES[mode_in]
        except KeyError:
            raise ValueError(f'Allowed options: ({", ".join(ALLOWED_MODES.keys())})')
        if mode_value == ModeValue.DEHUMIDIFY:
            speed_value = SpeedValue.DEHUM
        else:
            speed_in = input('What speed to select? ')
            try:
                speed_value = ALLOWED_SPEEDS[speed_in]
            except KeyError:
                raise ValueError(f'Allowed options: ({", ".join(ALLOWED_SPEEDS.keys())})')
        temp_in = input('What temperature to select? ')
        try:
            temp_value = int(temp_in)
        except ValueError:
            raise ValueError('Please enter a number (between 16 and 30)!')
        if temp_value < 16:
            temp_value = 16
        elif temp_value > 30:
            temp_value = 30
        command = ModeCommandPacket()
        command.mode = mode_value
        command.speed = speed_value
        command.temperature = temp_value
    elif command_in == 'off':
        command = OffCommandPacket()
    else:
        raise ValueError('Could not find specified command!')
    device = acquire_device()
    device.send_data(ir.decoder.ir_to_broadlink_full_packet(
        signals_in=command.encode_ir
    ))


def list_all_codes(debug=False):
    for file_name in sorted(os.listdir('codes')):
        command_packet = decoder.decode_file(os.path.join('codes', file_name))
        if debug:
            print('File:', file_name)
            print('Encoded:', command_packet)
            print('Log:', command_packet.parse_log)
        else:
            command_name = file_name.split(os.extsep)[0]
            print(f'{command_name}: {command_packet}')


def run_command(command_name):
    command_file = f'{command_name}{os.extsep}hex'
    command_packet = decoder.decode_file(os.path.join('codes', command_file))

    device = acquire_device()
    print('Sending data...')
    generated_packet = ir.decoder.ir_to_broadlink_full_packet(
        signals_in=command_packet.encode_ir
    )
    device.send_data(generated_packet)


def main():
    custom_command()


if __name__ == '__main__':
    main()
