# Reverse the order of bytes (often happens when working with raw bitcoin data)
def reverse_bytes(data):
    return ''.join(reversed([data[i:i+2] for i in range(0, len(data), 2)]))

# Convert a number to fit inside a field that is a specific number of bytes e.g. field(1, 4) = 00000001
def field(data, size):
    return format(data, '0' + str(size * 2) + 'x')

def create_block_header(version,prev_block,Merkle_Root,time,bits,nonce):
 header = reverse_bytes(field(version, 4)) + reverse_bytes(prev_block) + reverse_bytes(Merkle_Root) + reverse_bytes(field(time, 4)) + reverse_bytes(bits)+reverse_bytes(field(nonce, 4))
 #print(header)
 return header