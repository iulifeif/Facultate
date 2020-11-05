import traceback

from tema1.helper_functions import *

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 5005       # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    # cheile pentru cryptarile ECB si CBC
    key_dict = {
        "ECB": b"\ne\x8d3\xb2\xa8\xa5k\xfc\x9d0\x95\x15F\xf6A",
        "CBC": b"\x08\xfb3\nT.\xc3\xb4\xf3\xe5p\xc8\x96\xfd\xb9\xe3"
    }
    # cheia K3 pe care o au KM, A, B
    K3 = b"4h8f.093mJo:*9#$"
    # deschid conexiunea pentru A si B
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # asculta la portul 5005
        s.bind(("0.0.0.0", 5005))
        s.listen()
        while True:
            try:
                conn, addr = s.accept()
                with conn:
                    # primesc mesaj cu ce cheie se doreste criptarea
                    received_message = conn.recv(1024).decode()
                    # se face criptarea pentru cheia ceruta cu K3 si se trimite cheia criptata
                    # se creeaza o instanta a clasei de encrypt ca sa se salveze cheia de cryptare adica K3
                    encrypt = Encryptor(K3)
                    # apoi se apeleaza criptarea cu cheia ce trebuie criptata si tipul de criptare
                    # cu instanta clasei creata anterior
                    conn.sendall(encrypt.encrypt_message(key_dict[received_message], received_message))
            except Exception:
                print(traceback.format_exc())
