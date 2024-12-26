from Crypto.Random import get_random_bytes

key = get_random_bytes(16)  # 16 bytes = 128-bit key
print(key.hex())