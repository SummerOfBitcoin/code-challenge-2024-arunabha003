import os
import json
from Serialise import serialize_transaction
from coinbaseTxn import create_coinbase_hash
import hashlib

# Function to verify if total amount of inputs (vin) is greater than total amount of outputs (vout)
def verify_amount(transaction):
    total_input_amount = sum([vin['prevout']['value'] for vin in transaction['vin']])
    total_output_amount = sum([vout['value'] for vout in transaction['vout']])
    return total_input_amount >= total_output_amount

# Function to verify locktime based on Block Height
def verify_locktime(transaction):
    current_block_height = 839091
    locktime = transaction['locktime']
    return locktime < current_block_height

# Function to verify signature for each input of a transaction
def verify_signature(transaction):
    for index, vin in enumerate(transaction['vin']):
        scriptpubkey_type = vin['prevout']['scriptpubkey_type']
        if scriptpubkey_type == 'p2pkh':
            import p2pkh_verification
            signature = vin['scriptsig_asm'].split()[-3]
            public_key = vin['scriptsig_asm'].split()[-1]
            message = p2pkh_verification.serialize_transaction(transaction, index)
            if not p2pkh_verification.verify_ecdsa_signature(public_key, signature, message):
                return False
        elif scriptpubkey_type == 'v0_p2wpkh':
            import v0_p2wpkh_verification
            signature = vin['witness'][0]
            public_key = vin['witness'][1]
            message = v0_p2wpkh_verification.serialize_transaction(transaction, index)
            if not v0_p2wpkh_verification.verify_ecdsa_signature(public_key, signature, message):
                return False
        elif scriptpubkey_type == 'v1_p2tr':
            return True
        else:
            # Unknown scriptpubkey type
            return False
    return True

# Function to calculate the double SHA256 hash
def double_sha256(data):
    sha256_hash = hashlib.sha256(data).digest()
    return hashlib.sha256(sha256_hash).digest()

# Function to reverse byte order
def reverse_byte_order(hex_string):
    # Split the hex string into pairs of two characters
    byte_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

    # Reverse the order of the pairs
    reversed_byte_pairs = byte_pairs[::-1]

    # Concatenate the pairs back into a single string
    reversed_hex_string = ''.join(reversed_byte_pairs)
    return reversed_hex_string

# Main function to iterate through transactions in the mempool folder and verify them
def verify_transactions():
    valid_txn_folder = 'ValidTxn'

    if not os.path.exists(valid_txn_folder):
        os.makedirs(valid_txn_folder)

    mempool_folder = 'mempool'
    with open(os.path.join(valid_txn_folder, 'output1.txt'), 'w') as output_file, \
            open(os.path.join(valid_txn_folder, 'output2.txt'), 'w') as output2_file:
        # Get the hash of the coinbase transaction and write it to the output file

        coinbase_double_Hash = create_coinbase_hash()
        output_file.write(f"{coinbase_double_Hash}\n")
        reversed_hash = reverse_byte_order(coinbase_double_Hash)
        output2_file.write(f"{reversed_hash}\n")

        # Process other transactions
        for filename in os.listdir(mempool_folder):
            if filename.endswith('.json'):
                with open(os.path.join(mempool_folder, filename), 'r') as file:
                    try:
                        transaction = json.load(file)
                        if verify_amount(transaction) and verify_signature(transaction) and verify_locktime(
                                transaction):
                            serialized_tx = serialize_transaction(transaction)
                            double_sha256_hash = double_sha256(serialized_tx)
                            output_file.write(f"{double_sha256_hash.hex()}\n")
                            reversed_hash = reverse_byte_order(double_sha256_hash.hex())
                            output2_file.write(f"{reversed_hash}\n")
                    except Exception as e:
                        print(f"Error processing transaction {filename}: {e}")

if __name__ == "__main__":
    verify_transactions()
