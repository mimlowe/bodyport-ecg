
def read_compressed_file(input_path):
    with open(input_path, 'rb') as input_file:
        # Read the Huffman tree structure
        num_codes = int.from_bytes(input_file.read(2), byteorder='big')
        codes = {}
        for _ in range(num_codes):
            byte = input_file.read(1)[0]
            code_length = input_file.read(1)[0]
            code_bytes = input_file.read((code_length + 7) // 8)
            code = bin(int.from_bytes(code_bytes, byteorder='big'))[2:].zfill(code_length)
            codes[code] = byte

        # Read the compressed data
        compressed_data = input_file.read()

    return codes, compressed_data


def remove_padding(padded_data):
    return padded_data[1:]


def decode_data(encoded_data, codes):
    decoded_data = bytearray()
    current_code = ''

    for byte in encoded_data:
        for i in range(8):
            current_code += '1' if (byte & (128 >> i)) else '0'
            if current_code in codes:
                decoded_data.append(codes[current_code])
                current_code = ''

    return decoded_data


def decompress_file(input_path, output_path):
    codes, compressed_data = read_compressed_file(input_path)

    # Remove padding
    encoded_data = remove_padding(compressed_data)

    # Decode the data
    decoded_data = decode_data(encoded_data, codes)

    # Write the decompressed data to the output file
    with open(output_path, 'wb') as output_file:
        output_file.write(decoded_data)

    print(f"Decompressed file saved as: {output_path}")
    print(f"Decompressed size: {len(decoded_data)} bytes")
