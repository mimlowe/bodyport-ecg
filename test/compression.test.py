import filecmp
from ecg.compression.decompress_ecg import decompress_file


# Original File
input_file = '../sample_ecg_raw.bin'
# Compressed File
compressed_file = './compressed.bin'
# Decompressed File Path
decompressed_file = './decompressed.bin'

# Execute the decompression
decompress_file(compressed_file, decompressed_file)

# Compare with the original file to validate
if filecmp.cmp(input_file, decompressed_file):
    print("Decompression successful: The decompressed file is identical to the original.")
else:
    print("Error: The decompressed file differs from the original.")
