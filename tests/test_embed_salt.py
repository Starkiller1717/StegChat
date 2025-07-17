from src.stego.embed_png import embed_lsb
import os

# Generate a random 16-byte salt
salt = os.urandom(16)

# Embed salt into an image using LSB
embed_lsb("media/input_image.png", salt, "media/stego_salt.png")

# Save salt for later comparison/debugging
with open("media/salt.bin", "wb") as f:
    f.write(salt)

print("Salt embedded:", salt.hex())
