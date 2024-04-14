import os
import json

# Function to verify if total amount of inputs (vin) is greater than total amount of outputs (vout)
def verify_amount(transaction):
    total_input_amount = sum([vin['prevout']['value'] for vin in transaction['vin']])
    total_output_amount = sum([vout['value'] for vout in transaction['vout']])
    return total_input_amount >= total_output_amount

#Function to verify locktime based on Block Height
def verify_locktime(transaction):
    current_block_height=839091
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
            if not v0_p2wpkh_verification.verify_ecdsa_signature(public_key, signature,message):
                return False
        # elif scriptpubkey_type == 'p2sh':
        #     import verify_p2sh_signature
        #     if not verify_p2sh_signature.verify(transaction, vin):
        #         return False
        # elif scriptpubkey_type == 'v0_p2sh':
        #     import verify_v0_p2sh_signature
        #     if not verify_v0_p2sh_signature.verify(transaction, vin):
        #         return False
        elif scriptpubkey_type == 'v1_p2tr':
                return True
        else:
             # Unknown scriptpubkey type
            return False
    return True


# Main function to iterate through transactions in the mempool folder and verify them
def verify_transactions():
    result_folder = 'Results'
    output_file = os.path.join(result_folder, 'output.txt')


    with open(output_file, 'w') as output:
        mempool_folder = 'mempool'
        for filename in os.listdir(mempool_folder):
            if filename.endswith('.json'):
                with open(os.path.join(mempool_folder, filename), 'r') as file:
                    try:
                        transaction = json.load(file)
                        if verify_amount(transaction) and verify_signature(transaction) and verify_locktime(transaction):
                            output.write(f"Transaction {filename} is valid.\n")
                        else:
                            output.write(f"Transaction {filename} is invalid.\n")
                    except Exception as e:
                        output.write(f"Error processing transaction {filename}: {e}\n")

if __name__ == "__main__":
    verify_transactions()


