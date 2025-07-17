# Real‑time encrypted chat with dynamic 16‑byte salt exchange
import os, socket, struct, argparse
from src.stego.embed_png import embed_lsb
from src.stego.extract_png import extract_lsb
from src.crypto.kdf import derive_key
from src.crypto.encrypt import encrypt_message, decrypt_message

# ───────────────────────────────────────────────────────── helpers ──
def recv_exact(sock: socket.socket, n: int) -> bytes:
    data = b""
    while len(data) < n:
        chunk = sock.recv(n - len(data))
        if not chunk:
            raise ConnectionError("Socket closed")
        data += chunk
    return data

def framed_send(sock: socket.socket, blob: bytes):
    sock.sendall(struct.pack(">I", len(blob)) + blob)

def framed_recv(sock: socket.socket) -> bytes:
    length = struct.unpack(">I", recv_exact(sock, 4))[0]
    return recv_exact(sock, length)

# ───────────────────────────────────────────────────────── receiver ──
def start_receiver(password: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", port))
        s.listen(1)
        print(f"[Receiver] Listening on {port} ...")
        conn, addr = s.accept()
        with conn:
            print(f"[Receiver] Connected from {addr}")

            salt = recv_exact(conn, 16)
            key, _ = derive_key(password, salt)
            print(f"[Receiver] Session salt: {salt.hex()}")

            try:
                while True:
                    blob = framed_recv(conn)

                    if blob.startswith(b"IMG:"):
                        image_data = blob[4:]  # strip prefix
                        with open("media/received_output.png", "wb") as f:
                            f.write(image_data)
                        print("[Receiver] Image received and saved to media/received_output.png")
                        continue

                    try:
                        msg = decrypt_message(key, blob)
                        print(f"[Sender] {msg}")
                    except Exception as e:
                        print(f"[Error] Image decryption failed: {e}")

            except (ConnectionError, KeyboardInterrupt):
                print("\n[Receiver] Connection closed")

# ───────────────────────────────────────────────────────── sender ──
def start_sender(password: str, host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        print(f"[Sender] Connected to {host}:{port}")

        salt = os.urandom(16)
        s.sendall(salt)
        key, _ = derive_key(password, salt)
        print(f"[Sender] Session salt: {salt.hex()}")

        try:
            while True:
                msg = input("You: ")
                if msg.lower() == "exit":
                    break

                if msg.startswith("!img"):
                    plaintext = msg[4:].strip()
                    embed_lsb("media/input_image.png", plaintext.encode(), "media/stego_output.png")
                    with open("media/stego_output.png", "rb") as f:
                        img_bytes = f.read()
                    framed_send(s, b"IMG:" + img_bytes)
                    print("Data embedded and sent as image to receiver.")
                else:
                    ciphertext = encrypt_message(key, msg)
                    framed_send(s, ciphertext)
        except KeyboardInterrupt:
            pass
        finally:
            print("\n[Sender] Disconnected")

# ───────────────────────────────────────────────────────── CLI ──
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="StegChat – Encrypted Chat with Dynamic Salt")
    ap.add_argument("--mode", choices=["sender", "receiver"], required=True)
    ap.add_argument("--password", required=True)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5000)
    args = ap.parse_args()

    if args.mode == "receiver":
        start_receiver(args.password, args.port)
    else:
        start_sender(args.password, args.host, args.port)
