import hashlib

def create_coinbase_hash(amount, script_pub_key):
    serialized_data = ""

    # Version (little-endian)
    serialized_data += "01000000"

    # Number of inputs (always 1 for coinbase)
    serialized_data += "01"

    # Previous transaction hash (filled with zeros for coinbase)
    serialized_data += "0" * 64

    # Previous output index (maximum value for coinbase)
    serialized_data += "ffffffff"

    # Script length for empty coinbase input
    serialized_data += "00"

    # Sequence number (maximum value for coinbase)
    serialized_data += "ffffffff"

    # Number of outputs (always 1 for coinbase)
    serialized_data += "01"

    # Output amount (serialized)
    serialized_data += format(amount, '016x')[::-1]

    # ScriptPubKey length (half the length of the provided script)
    serialized_data += format(len(script_pub_key) // 2, '02x')

    # ScriptPubKey (output script)
    serialized_data += script_pub_key

    # Locktime (always zero for coinbase)
    serialized_data += "00000000"

    return double_sha256(serialized_data)


def Coinbase_hash(amount, script_pub_key):
    serialized_data = ""

    # Version (little-endian)
    serialized_data += "01000000"

    # Number of inputs (always 1 for coinbase)
    serialized_data += "01"

    # Previous transaction hash (filled with zeros for coinbase)
    serialized_data += "0" * 64

    # Previous output index (maximum value for coinbase)
    serialized_data += "ffffffff"

    # Script length for empty coinbase input
    serialized_data += "00"

    # Sequence number (maximum value for coinbase)
    serialized_data += "ffffffff"

    # Number of outputs (always 1 for coinbase)
    serialized_data += "01"

    # Output amount (serialized)
    serialized_data += format(amount, '016x')[::-1]

    # ScriptPubKey length (half the length of the provided script)
    serialized_data += format(len(script_pub_key) // 2, '02x')

    # ScriptPubKey (output script)
    serialized_data += script_pub_key

    # Locktime (always zero for coinbase)
    serialized_data += "00000000"

    return serialized_data



def double_sha256(data):
    hash1 = hashlib.sha256(data.encode()).digest()
    hash2 = hashlib.sha256(hash1).digest()
    return hash2.hex()



