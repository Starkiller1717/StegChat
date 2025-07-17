# test_crypto.py
# Placeholder for tests/test_crypto.py

from src.crypto.kdf import derive_key
from src.crypto.encrypt import encrypt_message, decrypt_message

password = "steghax123"
message = "Hello from the stego vault."

key, salt = derive_key(password)
ciphertext = encrypt_message(key, message)
plaintext = decrypt_message(key, ciphertext)

print("Original:", message)
print("Encrypted:", ciphertext.hex())
print("Decrypted:", plaintext)
