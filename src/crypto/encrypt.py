# encrypt.py
# Placeholder for src/crypto/encrypt.py

from nacl.secret import SecretBox
from nacl.utils import random as nacl_random

def encrypt_message(key: bytes, message: str) -> bytes:
    box = SecretBox(key)
    nonce = nacl_random(SecretBox.NONCE_SIZE)
    encrypted = box.encrypt(message.encode(), nonce)
    return encrypted

def decrypt_message(key: bytes, ciphertext: bytes) -> str:
    box = SecretBox(key)
    decrypted = box.decrypt(ciphertext)
    return decrypted.decode()
