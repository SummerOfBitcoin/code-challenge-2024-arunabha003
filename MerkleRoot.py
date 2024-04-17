import hashlib
import binascii
import os

def hashIt(firstTxHash, secondTxHash):
    # Reverse inputs before and after hashing
    # due to big-endian
    unhex_reverse_first = binascii.unhexlify(firstTxHash)[::-1]
    unhex_reverse_second = binascii.unhexlify(secondTxHash)[::-1]

    concat_inputs = unhex_reverse_first+unhex_reverse_second
    first_hash_inputs = hashlib.sha256(concat_inputs).digest()
    final_hash_inputs = hashlib.sha256(first_hash_inputs).digest()
    # reverse final hash and hex result
    return binascii.hexlify(final_hash_inputs[::-1])
 
 # Hash pairs of items recursively until a single value is obtained
def merkleCalculator(hashList):
    if len(hashList) == 1:
        return hashList[0]
    newHashList = []
    # Process pairs. For odd length, the last is skipped
    for i in range(0, len(hashList)-1, 2):
        newHashList.append(hashIt(hashList[i], hashList[i+1]))
    if len(hashList) % 2 == 1: # odd, hash last item twice
        newHashList.append(hashIt(hashList[-1], hashList[-1]))
    return merkleCalculator(newHashList)



# Transaction Hashes of block #100000
def compute_merkle_root(file_path):
    with open(file_path, 'r') as file:
        txids = [line.strip() for line in file]


    CalculatedMerkleRoot = str(merkleCalculator(txids), 'utf-8')
    #print(CalculatedMerkleRoot)

    return CalculatedMerkleRoot
   
