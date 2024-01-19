import heapq
import os
from collections import defaultdict, Counter
import pickle

class HuffmanNode:
    def __init__(self, char=None, freq=0, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def generate_huffman_tree(data):
    frequency = Counter(data)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, merged)

    return heap[0]

def generate_huffman_codes(root, current_code="", codes=None):
    if codes is None:
        codes = {}
    if root is not None:
        if root.char is not None:
            codes[root.char] = current_code
        generate_huffman_codes(root.left, current_code + "0", codes)
        generate_huffman_codes(root.right, current_code + "1", codes)
    return codes

def huffman_compress_file(input_path, output_path):
    with open(input_path, 'rb') as file:
        data = file.read()

    if not data:
        return

    huffman_tree = generate_huffman_tree(data)
    huffman_codes = generate_huffman_codes(huffman_tree)

    encoded_data = ''.join(huffman_codes[char] for char in data)

    with open(output_path, 'wb') as file:
        pickle.dump(huffman_codes, file)
        file.write(int(encoded_data, 2).to_bytes((len(encoded_data) + 7) // 8, byteorder='big'))

def huffman_decompress_file(input_path, output_path):
    with open(input_path, 'rb') as file:
        huffman_codes = pickle.load(file)
        padding_bits = int.from_bytes(file.read(1), byteorder='big')
        encoded_data_bytes = file.read()

    if not encoded_data_bytes:
        return

    # Convert encoded_data_bytes to a binary string
    encoded_data = ''.join(format(byte, '08b') for byte in encoded_data_bytes)

    root = generate_huffman_tree(huffman_codes.keys())
    current_node = root
    decoded_data = []

    for bit in encoded_data:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_data.append(current_node.char)
            current_node = root

    decoded_data = ''.join(map(str, decoded_data))  # Convert integers to characters

    # Remove padding bits from the end
    decoded_data = decoded_data[:-padding_bits]

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(decoded_data)
