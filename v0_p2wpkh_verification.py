import os
import json
import struct
import hashlib
import ecdsa


def serialize_transaction(transaction,index):
    serialized_tx = b''
    # Serialize version (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', transaction['version'])
    #print(serialized_tx.hex())

    #Serialize and hash for all the inputs TXID+VOUT 
    serialized_tx+=bytes.fromhex(hashlib.sha256(hashlib.sha256(serialize_TXID_VOUT(transaction['vin'])).digest()).hexdigest())
    #print(serialized_tx.hex())

    #Serialise input sequences
    serialized_tx+=bytes.fromhex(hashlib.sha256(hashlib.sha256(serialize_inputSequence(transaction['vin'])).digest()).hexdigest())
    #print(serialized_tx.hex())

    #Serialise hash for the target input's TXID+VOUT
    serialized_tx+=serialize_TXID_VOUT_TargetInput(transaction['vin'][index])
    #print(serialized_tx.hex())

    #Serialise Script Code
    
    serialized_tx+=bytes.fromhex('1976a914'+transaction['vin'][index]['prevout']['scriptpubkey'][4:] + '88ac')
    

    #Serialise Input Amount (little-endian 8 byte)
    serialized_tx += struct.pack('<Q', transaction['vin'][index]['prevout']['value'])
    #print(serialized_tx.hex())

    #Serialise Sequence for Target Input
    serialized_tx += struct.pack('<I', transaction['vin'][index]['sequence'])
    #print(serialized_tx.hex())

    # Serialize outputs
    serialized_tx += bytes.fromhex(hashlib.sha256(hashlib.sha256(serialize_outputs(transaction['vout'])).digest()).hexdigest())
    #print(serialized_tx.hex())

    # Serialize locktime (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', transaction['locktime'])
    #print(serialized_tx.hex())

    # Append Sign_Hash  (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', 1)

    single_hash=hashlib.sha256(serialized_tx).hexdigest()

    return single_hash

def reverse_byte_order(hex_string):
    # Split the hex string into pairs of two characters
    byte_pairs = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]

    # Reverse the order of the pairs
    reversed_byte_pairs = byte_pairs[::-1]

    # Concatenate the pairs back into a single string
    reversed_hex_string = ''.join(reversed_byte_pairs)
    return reversed_hex_string

def serialize_compact_size(size):
    if size < 0xfd:
        return bytes([size])
    elif size <= 0xffff:
        return b'\xfd' + struct.pack('<H', size)
    elif size <= 0xffffffff:
        return b'\xfe' + struct.pack('<I', size)
    else:
        return b'\xff' + struct.pack('<Q', size)


def serialize_TXID_VOUT_TargetInput(input):
    serialized_inputs = b''

    reversed_txid = reverse_byte_order(input['txid'])

        # Serialize reversed txid (little-endian 32 bytes)
    serialized_inputs += bytes.fromhex(reversed_txid)

        # Serialize vout (little-endian 4 bytes)
    serialized_inputs += struct.pack('<I', input['vout'])

    return serialized_inputs




def serialize_TXID_VOUT(inputs):
    serialized_inputs = b''

    for input in inputs:
        reversed_txid = reverse_byte_order(input['txid'])

        # Serialize reversed txid (little-endian 32 bytes)
        serialized_inputs += bytes.fromhex(reversed_txid)

        # Serialize vout (little-endian 4 bytes)
        serialized_inputs += struct.pack('<I', input['vout'])

    return serialized_inputs




def serialize_inputSequence(inputs):
    serialized_inputs = b''

    for input in inputs:

        # Serialize sequence (big-endian 4 bytes)
        serialized_inputs += struct.pack('<I', input['sequence'])

    return serialized_inputs




def serialize_outputs(outputs):
    serialized_outputs = b''

    for output in outputs:
        # Serialize value (little-endian 8 bytes)
        serialized_outputs += struct.pack('<Q', output['value'])

        # Serialize scriptPubKey length (varint)
        scriptpubkey_hex_length = len(output['scriptpubkey']) // 2
        serialized_outputs += encode_varint(scriptpubkey_hex_length)

        # Serialize scriptPubKey
        serialized_outputs += bytes.fromhex(output['scriptpubkey'])

    return serialized_outputs

def encode_varint(value):
    if value < 0xfd:
        return struct.pack('<B', value)
    elif value <= 0xffff:
        return b'\xfd' + struct.pack('<H', value)
    elif value <= 0xffffffff:
        return b'\xfe' + struct.pack('<I', value)
    else:
        return b'\xff' + struct.pack('<Q', value)



#########VERIFICATION PART#########
    

def parse_der_signature(serialized):
    # Extract the length of the R element
    r_length = int(serialized[6:8], 16) * 2
    # Calculate the start and end positions of R
    r_start = 8
    r_end = r_start + r_length
    # Extract R
    r = serialized[r_start:r_end]
    if r[0] == '0' and r[1]=='0':
        r = r[2:]

    # Extract the length of the S element
    s_length = int(serialized[r_end + 2:r_end + 4], 16) * 2
    # Calculate the start and end positions of S
    s_start = r_end + 4
    s_end = s_start + s_length
    # Extract S
    s = serialized[s_start:s_end]
    #print(r,s)

    r_bytes = bytes.fromhex(r)
    s_bytes = bytes.fromhex(s)
    return r_bytes,s_bytes




def verify_ecdsa_signature(public_key_hex, signature_hex, message_hex):
    """Verifies an ECDSA signature in Python."""
    r, s = parse_der_signature(signature_hex)
    message_bytes = bytes.fromhex(message_hex)

    vk = ecdsa.VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=ecdsa.SECP256k1, hashfunc=hashlib.sha256)
    try:
        vk.verify(r + s, message_bytes)
        return True  # Signature is valid
    except ecdsa.BadSignatureError:
        return False  # Signature is invalid





