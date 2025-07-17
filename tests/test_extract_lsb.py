from src.stego.extract_png import extract_lsb

# Adjust the path and number of bytes as needed
input_image = "media/received_output.png"
max_bytes = 512  # Adjust depending on how large the message might be

extracted = extract_lsb(input_image, max_bytes)
print("Extracted message:", extracted.decode(errors="ignore"))
