import os

import decoder
import ir

from device import acquire_device


def list_all_codes(debug=False):
    for file_name in sorted(os.listdir("codes")):
        command_packet = decoder.decode_file(os.path.join("codes", file_name))
        if debug:
            print("File:", file_name)
            print("Encoded:", command_packet)
            print("Log:", command_packet.parse_log)
        else:
            command_name = file_name.split(os.extsep)[0]
            print(f"{command_name}: {command_packet}")


def run_command(command_name):
    command_file = f"{command_name}{os.extsep}hex"
    command_packet = decoder.decode_file(os.path.join("codes", command_file))

    device = acquire_device()
    print("Sending data...")
    generated_packet = ir.decoder.ir_to_broadlink_full_packet(
        signals_in=command_packet.encode_ir
    )
    device.send_data(generated_packet)
