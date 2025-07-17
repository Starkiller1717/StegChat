from src.crypto.kdf import derive_key
from src.crypto.encrypt import decrypt_message
from src.stego.extract_png import extract_lsb

password = "stegopass123"
expected_length = 58  # Based on actual encryption output

# Reuse the same salt used during encryption
with open("media/salt.bin", "rb") as f:
    salt = f.read()

key, _ = derive_key(password, salt)

ciphertext = extract_lsb("media/stego_output.png", expected_length)

print("Extracted ciphertext length:", len(ciphertext))

# Decrypt
plaintext = decrypt_message(key, ciphertext)
print("Recovered Message:", plaintext)
