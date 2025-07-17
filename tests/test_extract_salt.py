from src.stego.extract_png import extract_lsb

# This should match the number of bytes we embedded
SALT_LENGTH = 16  

# Extract from image
salt = extract_lsb("media/stego_salt.png", SALT_LENGTH)
print("Extracted salt:", salt.hex())

