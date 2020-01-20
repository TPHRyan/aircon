def checksum(encoded_signal: str) -> int:
    if encoded_signal[:4] == 'S-I-':
        encoded_signal = encoded_signal[4:]
    bin_nybbles = map(''.join, zip(*(encoded_signal[i::4] for i in range(0, 4))))
    nybbles = (int(b, 2) for b in bin_nybbles)
    return sum(nybbles) % 16
