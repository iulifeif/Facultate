import hashlib

from tema1.helper_functions import *

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 5000


if __name__ == '__main__':
    # cheia K3 pe care o au KM, A, B
    K3 = b"4h8f.093mJo:*9#$"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 5000))
        s.listen()
        conn, addr = s.accept()
        with conn:
            # primeste modul de criptare de la A
            type_crypt =conn.recv(1024).decode()
            print("Modul de criptare primit de la A: ", type_crypt)
            # cere cheia de la KM criptata cu K3 si tipul de criptare potrivit
            key_code = get_key_from_KM(K3, type_crypt)
            # trimite mesajul lui A, pentru a-l anunta ca e gata de conversatie
            conn.sendall("Ready".encode())
            # se creaza o instanta a clasei de decriptare cu cheia potrivita modului de criptare
            decrypt = Decrytor(key_code)
            # creez buffer ul pentru a salva tot mesajul intr un loc
            buffer_message = b""
            # primeste un block criptat de la A
            message_from_A = conn.recv(1024)
            while message_from_A:
                # salvez in buffer block ul
                buffer_message += message_from_A
                # citeste urmatorul block de mesaj
                message_from_A = conn.recv(1024)
            # decriptez tot mesajul salvat de la A impreuna cu tipul de criptare
            message_from_A = decrypt.decrypt_message(buffer_message, type_crypt)
            # decodez mesajul si il printez
            print("Mesajul primit: ", message_from_A.decode())
