import hashlib
import os

from tema1.helper_functions import *

HOST = "0.0.0.0"  # The server's hostname or IP address
PORT = 5000        # The port used by the server


if __name__ == '__main__':
    key_dict = ["CBC", "ECB"]
    K3 = "4h8f.093mJo:*9#$"
    have_key = 0
    key_code = ""
    type_crypt = 0
    while not type_crypt or type_crypt not in key_dict:
        # type_crypt = input("Ce fel de criptare vrei sa se execute? (ECB/CBC): ").upper()
        type_crypt = "CBC"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_b:
        # se conecteaza cu portul 5000 adica B-ul
        socket_b.connect(("0.0.0.0", 5000))
        # trimite nodului B ce fel de criptare va folosi
        socket_b.sendall(type_crypt.encode())
        # trimit mesaj lui KM pentru a primi cheia corespunzatoare
        key_code = get_key_from_KM(K3, type_crypt, type_crypt)
        # primesc mesaj de la B pentru a continua conversatia
        message_from_B = socket_b.recv(1024).decode()
        print("Mesajul de la B: ", message_from_B)
        # in cazul in care nu primeste mesaj de start de la B, nu mai trimite nimic
        if message_from_B is not "Ready":
            raise Exception("B is not ready for conversation.")
        with open("tema1/fisier.txt", "rb") as f:
            buffer = b""
            message_for_B = f.read(16)
            block_count = 0
            while message_for_B:
                buffer += decrypt_message(K3, encrypt_message(K3, message_for_B))
                print("Trimis {} bytes: {}".format(len(message_for_B), message_for_B))
                # il criptez cu cheia de la KM, trimit lui B iv ul si mesajul criptat cu cheia de la KM
                socket_b.sendall(encrypt_message(key_code, message_for_B, type_crypt))
                block_count += 1
                message_for_B = f.read(16)
        print("Trimis {} blocuri: {}".format(block_count, buffer.decode("utf8")))
