import hashlib
import os

from helper_functions import *

HOST = "0.0.0.0"  # The server's hostname or IP address
PORT = 5000        # The port used by the server


if __name__ == '__main__':
    # modurile de criptare posibile
    key_dict = ["CBC", "ECB"]
    # cheia K3 pe care o au KM, A, B
    K3 = b"4h8f.093mJo:*9#$"
    key_code = ""
    type_crypt = 0
    # cat timp A ul nu primeste un tip de criptare valid
    # user ul trebuie sa introduca pana cand input ul este valid
    while not type_crypt or type_crypt not in key_dict:
        # adaug upper pentru cazul in care input ul este scris in litere mici
        # iar in lista sunt salvate cu litere mari si nu le vor gasi valide
        type_crypt = input("Ce fel de criptare vrei sa se execute? (ECB/CBC): ").upper()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_b:
        # se conecteaza la portul 5000 cu B-ul
        socket_b.connect(("0.0.0.0", 5000))
        # trimite nodului B ce fel de criptare va folosi, ceea ce a introdus user ul
        socket_b.sendall(type_crypt.encode())
        # trimit mesaj lui KM pentru a primi cheia corespunzatoare tipului de criptare introdus
        key_code = get_key_from_KM(K3, type_crypt)
        # creez instanta de encrypt cu cheia corespunzatoare modului de criptare introdus
        encrypt = Encryptor(key_code)
        # primesc mesaj de la B pentru a continua conversatia
        message_from_B = socket_b.recv(1024).decode()
        print("Mesajul de la B: ", message_from_B)
        # in cazul in care nu primeste mesaj de start de la B, nu mai trimite nimic
        if message_from_B != "Ready":
            raise Exception("B is not ready for conversation.")
        with open("fisier.txt", "rb") as f:
            # citesc din fisier mesajul
            all_message = f.read()
            # criptez mesajul cu tipul de criptare corespunzator
            message_for_B = encrypt.encrypt_message(all_message, type_crypt)
            # trimit lui B mesajul criptat in block uri de 16 bytes
            for index in range(0, len(message_for_B), 16):
                socket_b.sendall(message_for_B[index:index + 16])
        # printez mesajul criptat
        print("Mesajul criptat: ", message_for_B)
