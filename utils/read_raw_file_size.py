def get_file_size(file_object):
    file_object.seek(0, 2)  # Move to the end of the file
    size = file_object.tell()  # Get current position (file size)
    file_object.seek(0)  # Reset to the beginning
    return size
