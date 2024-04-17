import os
import hashlib

# Hash function used in the merkle root function (and in bitcoin in general)
def hash256(hex_str):
    binary = bytes.fromhex(hex_str)
    hash1 = hashlib.sha256(binary).digest()
    hash2 = hashlib.sha256(hash1).digest()
    result = hash2.hex()
    return result

# Reverse the order of bytes (often happens when working with raw bitcoin data)
def reverse_bytes(data):
    return ''.join(reversed([data[i:i+2] for i in range(0, len(data), 2)]))

def merkle_root(txids):
    # Exit Condition: Stop recursion when we have one hash result left
    if len(txids) == 1:
        # Convert the result to a string and return it
        return txids[0]

    # Keep an array of results
    result = []

    # 1. Split up array of hashes into pairs
    for i in range(0, len(txids), 2):
        one = txids[i]
        two = txids[i+1] if i+1 < len(txids) else one  # If there's only one left, use it again

        # 2. Concatenate each pair
        concat = one + two

        # 3. Hash the concatenated pair and add to results array
        result.append(hash256(concat))

    # Recursion: Do the same thing again for these results
    return merkle_root(result)

# Function to read txids from the "output.txt" file and compute the merkle root
def compute_merkle_root(file_path):
    with open(file_path, 'r') as file:
        txids = [line.strip() for line in file]

    # TXIDs must be in natural byte order when creating the merkle root
    reverse_bytes(txids)

    # Compute the merkle root
    #print(merkle_root(txids))
    return reverse_bytes(merkle_root(txids)) 


