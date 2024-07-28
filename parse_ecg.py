import struct


def read_24bit_signed(chunk):
    padded = chunk + b'\x00'
    value = struct.unpack('>i', padded)[0]
    return value >> 8


def read_24bit_samples(filename):
    samples = []
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(3)
            if not chunk or len(chunk) < 3:
                break
            sample = read_24bit_signed(chunk)
            samples.append(sample)
    return samples
