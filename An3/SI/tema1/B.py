import hashlib

from tema1.helper_functions import *

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 5000       # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    K3 = b"4h8f.093mJo:*9#$"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 5000))
        s.listen()
        conn, addr = s.accept()
        with conn:
            # primeste modul de criptare de la A
            type_crypt =conn.recv(1024).decode()
            print("Mesajul de la B: ", type_crypt)
            # cere cheia de la KM
            key_code = get_key_from_KM(K3, type_crypt)
            decrypt = Decrytor(key_code)
            conn.sendall("Ready".encode())
            message_from_A = conn.recv(32)
            buffer_message = b""
            block_count = 0
            while message_from_A:
                buffer_message += message_from_A
                message_from_A = conn.recv(32)
            message_from_A = decrypt.decrypt_message(buffer_message, type_crypt)
            print(message_from_A.decode())
        # print("Primit {} blocuri: {}".format(block_count, buffer_message.decode("utf8", errors="ignore")))
