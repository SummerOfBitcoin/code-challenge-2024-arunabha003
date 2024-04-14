import os
import json
import struct
import hashlib

def serialize_transaction(transaction):
    serialized_tx = b''

    # Serialize version (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', transaction['version'])

    # Serialize inputs count (variable)
    serialized_tx += serialize_compact_size(len(transaction['vin']))

    # Serialize inputs
    serialized_tx += serialize_inputs(transaction['vin'])

    # Serialize outputs count (variable)
    serialized_tx += serialize_compact_size(len(transaction['vout']))

    # Serialize outputs
    serialized_tx += serialize_outputs(transaction['vout'])

    # Serialize locktime (little-endian 4 bytes)
    serialized_tx += struct.pack('<I', transaction['locktime'])

    return serialized_tx

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

def serialize_inputs(inputs):
    serialized_inputs = b''

    for input in inputs:
        reversed_txid = reverse_byte_order(input['txid'])

        # Serialize reversed txid (little-endian 32 bytes)
        serialized_inputs += bytes.fromhex(reversed_txid)

        # Serialize vout (little-endian 4 bytes)
        serialized_inputs += struct.pack('<I', input['vout'])

        # Serialize scriptSig
        script_sig_length = len(input['scriptsig']) // 2
        serialized_inputs += serialize_compact_size(script_sig_length)
        serialized_inputs += bytes.fromhex(input['scriptsig'])

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

def serialize_transaction_from_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
        serialized_tx = serialize_transaction(data)
        return serialized_tx



