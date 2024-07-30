
class Node:
    """
    Node class for Huffman tree.
    """
    def __init__(self, byte, freq):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        """
        Override for less than operator.
        :param other:
        :return:
        """
        return self.freq < other.freq

