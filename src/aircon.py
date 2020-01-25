import decoder
import os


def main():
    for file_name in sorted(os.listdir('codes')):
        print('File:', file_name)
        command_packet = decoder.decode_file(os.path.join('codes', file_name))
        print('Encoded:', command_packet)
        print('Log:', command_packet.parse_log)


if __name__ == '__main__':
    main()
