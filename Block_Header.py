import struct

# Function to reverse byte order
def reverse_byte_order(hex_string):
    # Split the hex string into pairs of two characters
    byte_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

    # Reverse the order of the pairs
    reversed_byte_pairs = byte_pairs[::-1]

    # Concatenate the pairs back into a single string
    reversed_hex_string = ''.join(reversed_byte_pairs)
    return reversed_hex_string

# Function to create a block header
def create_block_header(version, prev_block, merkle_root, time, bits, nonce):
    # Serialize version (little-endian 4 bytes)
    serialized_version = struct.pack('<I', version)

    # Serialize previous block (natural byte order 32 bytes)
    serialized_prev_block = bytes.fromhex(prev_block)

    # Serialize merkle root (natural byte order 32 bytes)
    serialized_merkle_root = bytes.fromhex(merkle_root)

    # Serialize time (little-endian 4 bytes)
    serialized_time = struct.pack('<I', time)

    # Serialize bits (little-endian 4 bytes)
    serialized_bits = struct.pack('<I', bits)

    # Serialize nonce (little-endian 4 bytes)
    serialized_nonce = struct.pack('<I', nonce)

    # Concatenate all serialized fields
    block_header = serialized_version + serialized_prev_block + serialized_merkle_root + serialized_time + serialized_bits + serialized_nonce

    # print(block_header.hex())
    return block_header

# # Example usage:
# version = 1
# prev_block = '00000000000000000ecdf6f7b15f10fd99b10cfd4f76050a1696b5cc22f29808'
# merkle_root = 'e1de7d3f1a89ed48233c4ed8755309e37ecf50c6e7617167dffe778682ca276f'
# time = 1446952553
# bits = 0x1811a954
# nonce = 3704665741

