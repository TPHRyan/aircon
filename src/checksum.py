def checksum(encoded_signal: str) -> str:
    if encoded_signal[:4] == 'S-I-':
        encoded_signal = encoded_signal[4:]
    bin_nybbles = map(''.join, zip(*(encoded_signal[i::4] for i in range(0, 4))))
    nybbles = (int(b, 2) for b in bin_nybbles)
    nybble_sum = sum(nybbles)
    print(nybble_sum)
    return f'{nybble_sum % 16:0>4b}'
