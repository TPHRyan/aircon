import decoder
import os


def main():
    for file_name in os.listdir('codes'):
        print('File:', file_name)
        print('Encoded:', decoder.decode_file(os.path.join('codes', file_name)))


if __name__ == '__main__':
    main()
