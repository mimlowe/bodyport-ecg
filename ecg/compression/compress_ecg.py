from collections import Counter
import heapq
from ecg.compression.node import Node


def read_file_bytes(file_path):
    """
    Read the bytes of a file
    :param file_path: String
    :return: File bytes
    """
    with open(file_path, 'rb') as file:
        return file.read()


def count_byte_frequencies(data):
    """
    Count the frequency of each byte in the data
    :param data:
    :return:
    """
    return Counter(data)


def generate_huffman_codes(root):
    """
    Generate Huffman codes for each byte in the tree
    :param root: Root node of the Huffman tree
    :return: dictionary of Huffman codes
    """
    codes = {}

    def traverse(node, code):
        if node.byte is not None:
            codes[node.byte] = code
            return

        traverse(node.left, code + '0')
        traverse(node.right, code + '1')

    traverse(root, '')
    return codes


def build_huffman_tree(freq_dict):
    """
    Build a Huffman tree from a frequency dictionary
    :param freq_dict:
    :return:
    """
    heap = [Node(byte, freq) for byte, freq in freq_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)

    return heap[0]


def encode_data(data, codes):
    """
    Encode data using Huffman codes
    :param data: File bytes
    :param codes: Huffman code dictionary
    :return:
    """
    encoded = ''
    for byte in data:
        encoded += codes[byte]
    return encoded


def pad_encoded_data(encoded_data):
    """
    Pad the encoded data to a multiple of 8 bits
    :param encoded_data:
    :return:
    """
    padding = 8 - (len(encoded_data) % 8)
    if padding == 8:
        padding = 0
    padded_info = bytes([padding])
    encoded_data += '0' * padding
    padded_encoded = int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder='big')
    return padded_info + padded_encoded


def write_compressed_file(output_path, byte_array, codes):
    """
    Write the compressed data to a file, including the Huffman tree structure
    :param output_path: String, path to write the compressed file
    :param byte_array: input data
    :param codes: Huffman code dictionary
    :return:
    """
    with open(output_path, 'wb') as output_file:
        # Write the Huffman tree structure
        output_file.write(len(codes).to_bytes(2, byteorder='big'))
        for byte, code in codes.items():
            output_file.write(byte.to_bytes(1, byteorder='big'))
            output_file.write(len(code).to_bytes(1, byteorder='big'))
            output_file.write(int(code, 2).to_bytes((len(code) + 7) // 8, byteorder='big'))

        # Write the compressed data
        output_file.write(byte_array)


def compress_file(input_path, output_path):
    """
    Compress a file using Huffman coding
    :param input_path: String
    :param output_path: String
    :return: Compression metadata html string
    """

    # Read the input file as a byte array
    data = read_file_bytes(input_path)

    # Count the frequency of each byte in the data
    freq_dict = count_byte_frequencies(data)

    # Build the Huffman tree
    root = build_huffman_tree(freq_dict)

    # Generate Huffman codes for each byte
    codes = generate_huffman_codes(root)

    # Encode and pad the data
    encoded_data = encode_data(data, codes)
    padded_data = pad_encoded_data(encoded_data)

    # Write the compressed data to a file
    write_compressed_file(output_path, padded_data, codes)

    # Calculate compression metadata
    original_size = len(data)
    compressed_size = len(padded_data) + sum(len(code) for code in codes.values()) // 8 + 2
    compression_ratio = (1 - compressed_size / original_size) * 100

    # Return compression results metadata
    return original_size, compressed_size, compression_ratio

