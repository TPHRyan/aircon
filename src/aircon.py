import broadlink
import decoder
import ir.decoder
import os
import time


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

    device: broadlink.rm2 = broadlink.discover()
    tries = 0
    while not hasattr(device, 'send_data') and tries < 3:
        device = broadlink.discover()
        tries += 1
    if not hasattr(device, 'send_data'):
        raise RuntimeError(f'Device {device.type} is not supported!')
    print('Device found! Authenticating...')
    auth = device.auth()
    tries = 0
    while auth is None and tries < 3:
        print('Device not authenticated, retrying...')
        time.sleep(1)
        device.auth()
        tries += 1
    if tries >= 3:
        raise RuntimeError('Could not find device!')
    print('Sending data...')
    generated_packet = ir.decoder.ir_to_broadlink_full_packet(
        signals_in=command_packet.encode_ir
    )
    device.send_data(generated_packet)


def main():
    run_command('on')
    time.sleep(1)
    run_command('cool_25')


if __name__ == '__main__':
    main()
