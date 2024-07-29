import struct


def read_24bit_signed(chunk):
    """
    This function reads a 24-bit signed integer from a 3-byte chunk.
    :param chunk:
    :return:
    """
    padded = chunk + b'\x00'
    value = struct.unpack('>i', padded)[0]
    return value >> 8


def read_24bit_samples(filename):
    """
    This function reads a sequence of 24-bit signed samples from a file.
    :param filename:
    :return: Array of integers
    """
    samples = []
    with open(filename, 'rb') as file:
        while True:
            chunk = file.read(3)
            if not chunk or len(chunk) < 3:
                break
            sample = read_24bit_signed(chunk)
            samples.append(sample)
    return samples


def read_samples(file):
    """
    This function reads a sequence of 24-bit signed samples from a file.
    :param filename:
    :return: Array of integers
    """
    samples = []
    while True:
        chunk = file.read(3)
        if not chunk or len(chunk) < 3:
            break
        sample = read_24bit_signed(chunk)
        samples.append(sample)
    return samples
