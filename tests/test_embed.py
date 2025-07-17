from src.crypto.kdf import derive_key
from src.crypto.encrypt import encrypt_message
from src.stego.embed_png import embed_lsb

password = "stegopass123"
message = "Top Secret Payload"
key, salt = derive_key(password)

ciphertext = encrypt_message(key, message)
embed_lsb("media/input_image.png", ciphertext, "media/stego_output.png")
print("Encrypted byte length:", len(ciphertext))

# Save the salt so we can reuse it later
with open("media/salt.bin", "wb") as f:
    f.write(salt)
