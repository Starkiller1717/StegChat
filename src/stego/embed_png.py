# embed_png.py
# Placeholder for src/stego/embed_png.py

from PIL import Image
import os

def to_bitstream(data: bytes) -> str:
    return ''.join(f"{byte:08b}" for byte in data)

def embed_lsb(image_path: str, data: bytes, output_path: str):
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = img.load()

    width, height = img.size
    bitstream = to_bitstream(data)
    total_bits = len(bitstream)

    if total_bits > width * height * 3:
        raise ValueError("Data too large to embed in image.")

    bit_index = 0
    for y in range(height):
        for x in range(width):
            if bit_index >= total_bits:
                break

            r, g, b = pixels[x, y]
            r = (r & ~1) | int(bitstream[bit_index])     # Red channel
            bit_index += 1

            if bit_index < total_bits:
                g = (g & ~1) | int(bitstream[bit_index]) # Green channel
                bit_index += 1

            if bit_index < total_bits:
                b = (b & ~1) | int(bitstream[bit_index]) # Blue channel
                bit_index += 1

            pixels[x, y] = (r, g, b)

        if bit_index >= total_bits:
            break

    img.save(output_path)
    print(f"Data embedded and saved to {output_path}")
