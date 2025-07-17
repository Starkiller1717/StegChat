# extract_png.py
# Placeholder for src/stego/extract_png.py

from PIL import Image

def extract_lsb(image_path: str, length: int) -> bytes:
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load()

    width, height = img.size
    bitstream = ""

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= length * 8:
                break

            r, g, b = pixels[x, y]
            bitstream += str(r & 1)
            bit_index += 1

            if bit_index < length * 8:
                bitstream += str(g & 1)
                bit_index += 1

            if bit_index < length * 8:
                bitstream += str(b & 1)
                bit_index += 1

        if bit_index >= length * 8:
            break

    # Convert bitstream to bytes
    data = bytes(int(bitstream[i:i+8], 2) for i in range(0, len(bitstream), 8))
    return data
