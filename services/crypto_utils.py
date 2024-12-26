import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Hash import HMAC, SHA256
from dotenv import load_dotenv

import base64
import hashlib
#generate key from file generate_keys.py and put it in .env file
# Get key from environment variable
load_dotenv()
print(os.getenv)
IV = base64.b64decode(os.environ.get('IV_KEY'))

# Secret key for HMAC (should be stored securely and shared between client and server)
HMAC_SECRET_KEY = base64.b64decode(os.getenv('HMAC_KEY'))

def encrypt_data(data: str,) -> dict:
    cipher = AES.new(IV, AES.MODE_CBC, IV)
    encrypted = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))

    # Generate HMAC of the encrypted data
    hmac = HMAC.new(HMAC_SECRET_KEY, encrypted, SHA256)
    hmac_digest = hmac.digest()

    # Return both encrypted data (base64) and HMAC (base64)
    return {
        "encrypted_data": base64.b64encode(encrypted).decode('utf-8'),
        "hmac": base64.b64encode(hmac_digest).decode('utf-8')
    }

def decrypt_data(encrypted_data: str, hmac_digest: str, key: bytes) -> str:
    # Decode from base64
    encrypted_data = base64.b64decode(encrypted_data)
    expected_hmac = base64.b64decode(hmac_digest)

    # Verify HMAC
    hmac = HMAC.new(HMAC_SECRET_KEY, encrypted_data, SHA256)
    try:
        hmac.verify(expected_hmac)  # This will throw if the data was tampered with
    except ValueError:
        raise ValueError("HMAC verification failed: Data has been tampered with")

    # Decrypt the data
    cipher = AES.new(key, AES.MODE_CBC, IV)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)

    return decrypted.decode('utf-8')