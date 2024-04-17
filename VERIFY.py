import hashlib


def hash256(data):
    binary = bytes.fromhex(data)
    hash1 = hashlib.sha256(binary).digest()
    hash2 = hashlib.sha256(hash1).hexdigest()
    return hash2

def reverse_bytes(data):
    return ''.join(reversed([data[i:i+2] for i in range(0, len(data), 2)]))

hash=reverse_bytes(hash256("000000200000000000000000000000000000000000000000000000000000000000000000f9224c7e25e7159d2f1b6e7ea9a26cab04a46d62e4fa18c82717f32ccaeb85d46f071b66ffff001f71cb0000"))
print(hash)