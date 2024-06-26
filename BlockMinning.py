import hashlib
import MerkleRoot
import os
import time


# Target hash
#target = '0000ffff00000000000000000000000000000000000000000000000000000000'
# Utility Functions


def get_unix_time():
    return int(time.time())

# The hash function used in mining (convert hexadecimal to binary first, then SHA256 twice)
def hash256(data):
    binary = bytes.fromhex(data)
    hash1 = hashlib.sha256(binary).digest()
    hash2 = hashlib.sha256(hash1).hexdigest()
    return hash2

# Convert a number to fit inside a field that is a specific number of bytes e.g. field(1, 4) = 00000001
def field(data, size):
    return format(data, '0' + str(size * 2) + 'x')

# Reverse the order of bytes (often happens when working with raw bitcoin data)
def reverse_bytes(data):
    return ''.join(reversed([data[i:i+2] for i in range(0, len(data), 2)]))

def reverse_hex(data):
    byte_data = bytes.fromhex(data)
    reversed_bytes = bytes(reversed(byte_data))
    return reversed_bytes.hex()

# Function to mine for a block with the given target hash
def mine_block(target):
    # Path to the "output.txt" file inside the "ValidTx" folder
    output_file_path = os.path.join('ValidTxn', 'output2.txt')

    # Block Header (Fields)
    version    = 0x20000000
    prevblock  = '0000000000000000000000000000000000000000000000000000000000000000'
    merkleroot = MerkleRoot.compute_merkle_root(output_file_path) 
    time       = get_unix_time()  
    bits       = '1f00ffff'
    nonce      = 0             #274148111

    # Block Header (Serialized)
    header = reverse_bytes(field(version, 4)) + reverse_bytes(prevblock) + merkleroot + reverse_bytes(field(time, 4)) + reverse_bytes(bits)
    #print(header)

    # Mine!
    while True:
        # hash the block header
        attempt = header + reverse_bytes(field(nonce, 4))
        result = reverse_bytes(hash256(attempt))

        # show result
        #print(f"{nonce}: {result}")

        # end if we get a block hash below the target
        if int(result,16) < int(target,16):
            return nonce

        # increment the nonce and try again...
        nonce += 1

        # Remove the previously added nonce before the next iteration
        attempt = attempt[:-8] # Assuming nonce is represented by 4 bytes (8 hexadecimal characters)


# # Mine for the block with the given target hash
# mined_nonce = mine_block(target)
# print(f"Nonce for target hash {target}: {mined_nonce}")
