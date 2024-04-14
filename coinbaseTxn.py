import hashlib

def create_coinbase_hash():
    version = "01000000"
    marker = "00"
    flag = "01"
    input_count = "01"
    input_val = "0000000000000000000000000000000000000000000000000000000000000000"
    vout = "ffffffff"
    script_size = "19"
    current_block_height = "b3cd0c"  # In little_endian
    script_sig = "03" + current_block_height + "184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100"
    sequence = "ffffffff"
    output_count = "02"
    amount1 = "f595814a00000000"
    script_pubkey_size1 = "19"
    script_pubkey1 = "76a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac"
    amount2 = "0000000000000000"
    script_pubkey_size2 = "26"
    script_pubkey2 = "6a24aa21a9edfaa194df59043645ba0f58aad74bfd5693fa497093174d12a4bb3b0574a878db"
    stack_item = "01"
    size = "20"
    item_zero = "0000000000000000000000000000000000000000000000000000000000000000"
    locktime = "00000000"

    # Concatenate the values into a single string
    concatenated_values = (
        version + marker + flag + input_count + input_val + vout + script_size +
        script_sig + sequence + output_count + amount1 + script_pubkey_size1 +
        script_pubkey1 + amount2 + script_pubkey_size2 + script_pubkey2 + stack_item +
        size + item_zero + locktime
    )

    # Convert the concatenated string into bytes
    concatenated_bytes = bytes.fromhex(concatenated_values)

    # Compute the double SHA256 hash of the bytes
    hash_result = hashlib.sha256(hashlib.sha256(concatenated_bytes).digest()).digest()

    # Return the double SHA256 hash as a hexadecimal string
    return hash_result.hex()


def Coinbase_hash():
    version = "01000000"
    marker = "00"
    flag = "01"
    input_count = "01"
    input_val = "0000000000000000000000000000000000000000000000000000000000000000"
    vout = "ffffffff"
    script_size = "19"
    current_block_height = "b3cd0c"  # In little_endian
    script_sig = "03" + current_block_height + "184d696e656420627920416e74506f6f6c373946205b8160a4256c0000946e0100"
    sequence = "ffffffff"
    output_count = "02"
    amount1 = "f595814a00000000"
    script_pubkey_size1 = "19"
    script_pubkey1 = "76a914edf10a7fac6b32e24daa5305c723f3de58db1bc888ac"
    amount2 = "0000000000000000"
    script_pubkey_size2 = "26"
    script_pubkey2 = "6a24aa21a9edfaa194df59043645ba0f58aad74bfd5693fa497093174d12a4bb3b0574a878db"
    stack_item = "01"
    size = "20"
    item_zero = "0000000000000000000000000000000000000000000000000000000000000000"
    locktime = "00000000"

    # Concatenate the values into a single string
    concatenated_values = (
        version + marker + flag + input_count + input_val + vout + script_size +
        script_sig + sequence + output_count + amount1 + script_pubkey_size1 +
        script_pubkey1 + amount2 + script_pubkey_size2 + script_pubkey2 + stack_item +
        size + item_zero + locktime
    )

   


   
    return concatenated_values


# # Test the functions
# double_sha256 = create_coinbase_hash()
# print("Double SHA256 hash:", double_sha256)

# hash_concatenated = Coinbase_hash()
# print("Hash after concatenating:", hash_concatenated)
