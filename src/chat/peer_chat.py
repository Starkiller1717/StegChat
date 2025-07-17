import os, socket, struct, threading, argparse
from src.crypto.kdf import derive_key
from src.crypto.encrypt import encrypt_message, decrypt_message
from src.stego.embed_png import embed_lsb
from src.stego.extract_png import extract_lsb

# ────────────────────────────────────────────────────────────────
# HELPERS

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

# ────────────────────────────────────────────────────────────────
# MAIN CHAT PEER FUNCTIONALITY

def handle_send(sock: socket.socket, key: bytes):
    while True:
        msg = input("You: ")
        if msg.lower() == "exit":
            break

        if msg.startswith("!img"):
            plaintext = msg[4:].strip().encode()
            embed_lsb("media/input_image.png", plaintext, "media/stego_output.png")
            with open("media/stego_output.png", "rb") as f:
                data = f.read()
            framed_send(sock, b"IMG:" + data)
            print("[Sender] Image sent to peer.")
        else:
            ciphertext = encrypt_message(key, msg)
            framed_send(sock, b"TXT:" + ciphertext)


def handle_recv(sock: socket.socket, key: bytes):
    try:
        while True:
            data = framed_recv(sock)
            if data.startswith(b"IMG:"):
                with open("media/received_output.png", "wb") as f:
                    f.write(data[4:])
                print("\n[Peer] Image received and saved to media/received_output.png")
            elif data.startswith(b"TXT:"):
                msg = decrypt_message(key, data[4:])
                print(f"\n[Peer] {msg}")
    except (ConnectionError, KeyboardInterrupt):
        print("\n[Peer] Disconnected")


def run_peer(password: str, host: str, port: int, listen: bool):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if listen:
            s.bind((host, port))
            s.listen(1)
            print(f"[Peer] Listening on {host}:{port} ...")
            conn, _ = s.accept()
        else:
            s.connect((host, port))
            conn = s

        print("[Peer] Connected. Performing key derivation ...")

        salt = os.urandom(16)
        conn.sendall(salt)
        if listen:
            salt = recv_exact(conn, 16)
        key, _ = derive_key(password, salt)

        threading.Thread(target=handle_recv, args=(conn, key), daemon=True).start()
        handle_send(conn, key)

# ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="StegChat – Bi-Directional Peer Chat")
    ap.add_argument("--password", required=True)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=5000)
    ap.add_argument("--listen", action="store_true")
    args = ap.parse_args()

    run_peer(args.password, args.host, args.port, args.listen)
