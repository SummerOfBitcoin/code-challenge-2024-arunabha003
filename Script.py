from Block_Header import create_block_header
from coinbaseTxn import Coinbase_hash
import MerkleRoot
import BlockMinning
import os

# Function to write data to output.txt
def write_to_output(data):
    with open("output.txt", "a") as file:  # Open file in append mode to add data
        file.write(data + "\n")

# Path to the "output.txt" file inside the "ValidTx" folder
output_file_path1 = os.path.join('ValidTxn', 'output1.txt')

# 1. Get hash from create_block_header function
version = 0x20000000
prev_block = '0000000000000000000000000000000000000000000000000000000000000000'
merkle_root = MerkleRoot.compute_merkle_root(output_file_path1)
time = 1713047407
bits = 0x1f00ffff
nonce = BlockMinning.mine_block('0000ffff00000000000000000000000000000000000000000000000000000000')
block_header = create_block_header(version, prev_block, merkle_root, time, bits, nonce)
block_header_hash = block_header.hex()
write_to_output(block_header_hash)

# 2. Get hash from Coinbase_hash function
coinbase_amount = 100000000  # Example amount in satoshis
coinbase_script_pub_key = "76a9144c98213638e76470d0ec8de74c14e08c8a06435b88ac"
coinbase_hash = Coinbase_hash(coinbase_amount, coinbase_script_pub_key)
write_to_output(coinbase_hash)

# 3. Read data from ValidTxn/output2.txt and append to output.txt
results_file_path = os.path.join("ValidTxn", "output2.txt")
with open(results_file_path, "r") as results_file:
    for line in results_file:
        write_to_output(line.strip())
