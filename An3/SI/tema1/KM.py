import socket
import traceback

from Crypto import Random
from Crypto.Cipher import AES

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 5005       # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    key_dict = {
        "ECB": "Sixteen byte key",
        "CBC": "Sixteen byte key"
    }
    K3 = "4h8f.093mJo:*9#$"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 5005))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    received_message = conn.recv(1024).decode()
                    print("[KM] Am primit: " + received_message)
                    # if received_message in key_dict:
                    # se face criptarea pentru cheia ceruta cu K3
                    iv = Random.new().read(AES.block_size)
                    aes = AES.new(K3, AES.MODE_CBC, iv)
                    send_message = aes.encrypt(key_dict[received_message])
                    conn.sendall(iv + send_message)
                    print("Am trimis", len(iv + send_message), "bytes")
            except Exception:
                print(traceback.format_exc())
