import hashlib
import MerkleRoot  # Assuming this is a module for calculating Merkle Root
import os


# Target hash (Adjust difficulty by changing the number of leading zeros)
#target = '0000' + '0' * 60  # 64 leading zeros for extreme difficulty

# Utility Functions

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

# Function to mine for a block with the given target hash
def mine_block(target):
  # Path to the "output.txt" file inside the "ValidTx" folder
  output_file_path = os.path.join('ValidTxn', 'output1.txt')

  # Block Header (Fields)
  version = 0x20000000
  prevblock = '0000000000000000000000000000000000000000000000000000000000000000'
  merkleroot = MerkleRoot.compute_merkle_root(output_file_path)
  time = 1713047407
  bits = '1f00ffff'
  nonce = 0

  # Block Header (Serialized)
  header = reverse_bytes(field(version, 4)) + reverse_bytes(prevblock) + reverse_bytes(merkleroot) + reverse_bytes(field(time, 4)) + reverse_bytes(bits)

  # Separate variable for attempt
  attempt = header

  while True:
    # Update attempt with new nonce
    attempt += reverse_bytes(field(nonce, 4))

    # Hash the block header
    result = reverse_bytes(hash256(attempt))

    # Convert hash result to integer for comparison (leading zeros are significant)
    result_int = int(result, 16)

    # Check if hash is below the target (less than target integer)
    if result_int < int(target, 16):
      return nonce

    # Increment the nonce and try again...
    nonce += 1

# Example usage (assuming MerkleRoot.compute_merkle_root is implemented)
# mined_nonce = mine_block(target)
# print(f"Mined a block with nonce: {mined_nonce}")
