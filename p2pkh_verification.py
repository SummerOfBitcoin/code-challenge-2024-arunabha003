import os
import json
import struct
import hashlib
import ecdsa 


def serialize_transaction(transaction,index):
    serialized_tx = b'' 
    
    # Serialize version (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', transaction['version'])

    # Serialize inputs count (variable)
    serialized_tx += serialize_compact_size(len(transaction['vin']))

    for i in range(len(transaction['vin'])):
        input = transaction['vin'][i]

        # Serialize based on index (optional)
        if i == index:  # Include optional index check if needed
            serialized_tx += serialize_inputs(input)
            # print("Index" , i, "is serialised")
        else:
            serialized_tx += serialize_Subinputs(input) 
            # print("Index" , i, "is Subserialised")  

    # Serialize outputs count (variable)
    serialized_tx += serialize_compact_size(len(transaction['vout']))

    # Serialize outputs
    serialized_tx += serialize_outputs(transaction['vout'])

    # Serialize locktime (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', transaction['locktime'])

    # Append Sign_Hash  (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', 1)

    # # Double hash and store the hash (if P2PKH)
    # double_hash = hashlib.sha256(serialized_tx).hexdigest()
    single_hash=hashlib.sha256(serialized_tx).hexdigest()

    return single_hash


def reverse_byte_order(hex_string):
    # Split the hex string into pairs of two characters
    byte_pairs = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]

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


def serialize_inputs(inputs):
    serialized_inputs = b''

    
    reversed_txid = reverse_byte_order(inputs['txid'])
   
    # Serialize reversed txid (little-endian 32 bytes)
    serialized_inputs += bytes.fromhex(reversed_txid)

     # Serialize vout (little-endian 4 bytes)
    serialized_inputs += struct.pack('<I', inputs['vout'])

     # Serialize scriptSig (length based on prevout['scriptpubkey'])
    script_sig_length = len(inputs['prevout']['scriptpubkey']) // 2
    serialized_inputs += serialize_compact_size(script_sig_length)
    serialized_inputs += bytes.fromhex(inputs['prevout']['scriptpubkey'])

     # Serialize sequence (big-endian 4 bytes)
    serialized_inputs += struct.pack('<I', inputs['sequence'])

    return serialized_inputs


#Extra function

def serialize_Subinputs(inputs):
    serialized_inputs = b''
    reversed_txid = reverse_byte_order(inputs['txid'])

    # Serialize reversed txid (little-endian 32 bytes)
    serialized_inputs += bytes.fromhex(reversed_txid)

    # Serialize vout (little-endian 4 bytes)
    serialized_inputs += struct.pack('<I', inputs['vout'])

    # Serialize scriptSig
    # script_sig_length = len(inputs['scriptsig']) // 2
    # serialized_inputs += serialize_compact_size(script_sig_length)
    # serialized_inputs += bytes.fromhex(input['scriptsig'])

    #script_sig_length
    serialized_inputs+=bytes.fromhex("00")


    # Serialize sequence (big-endian 4 bytes)
    serialized_inputs += struct.pack('<I', inputs['sequence'])

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









