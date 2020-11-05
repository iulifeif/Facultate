import traceback

from tema1.helper_functions import *

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 5005       # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    key_dict = {
        "ECB": b"Sixteen byte key",
        "CBC": b"Sixteen byte key"
    }
    K3 = b"4h8f.093mJo:*9#$"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 5005))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    # primesc mesaj cu ce cheie se doreste criptarea
                    received_message = conn.recv(1024).decode()
                    # se face criptarea pentru cheia ceruta cu K3 si se trimite
                    encrypt = Encryptor(K3)
                    conn.sendall(encrypt.encrypt_message(key_dict[received_message], received_message))
            except Exception:
                print(traceback.format_exc())
