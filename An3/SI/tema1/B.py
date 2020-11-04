import hashlib

from tema1.helper_functions import *

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 5000       # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    K3 = "4h8f.093mJo:*9#$"
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
            conn.sendall("Ready".encode())
            message_from_A = conn.recv(32)
            buffer_message = b""
            block_count = 0
            while message_from_A:
                decrypted_message = decrypt_message(key_code, message_from_A, type_crypt)
                buffer_message += decrypted_message
                print("Primit {} bytes: {}".format(len(decrypted_message), decrypted_message))
                block_count += 1
                message_from_A = conn.recv(32)
        print("Primit {} blocuri: {}".format(block_count, buffer_message.decode("utf8", errors="ignore")))
