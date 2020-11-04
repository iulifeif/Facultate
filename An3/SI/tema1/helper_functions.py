import socket
from Crypto import Random
from Crypto.Cipher import AES


def get_key_from_KM(K3, encryption_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_KM:
        # se conteaza la portul 5005 unde este KM
        socket_KM.connect(("0.0.0.0", 5005))
        # ii trimite lui KM modul de criptare ales
        socket_KM.sendall(encryption_type.encode())
        # primeste de la KM cheia impreuna cu iv
        message_key = socket_KM.recv(1024)
    # ii face decode pentru a fi de tip string cheia de la KM
    return decrypt_message(K3, message_key, encryption_type).decode()


def decrypt_message(key_code, message_for_decryption, decryption_type):
    iv = message_for_decryption[:16]
    if decryption_type == "CBC":
        aes = AES.new(key_code, AES.MODE_CBC, iv)
    else:
        aes = AES.new(key_code, AES.MODE_ECB, iv)
    # decripteaza mesajul, il decodeaza pentru a fi string, scoate spatiile de la final in caz ca sunt
    # si il encodeaza din nou pentru a fi iar binar
    return aes.decrypt(message_for_decryption[16:]).strip(chr(0).encode("utf8"))


def encrypt_message(key_code, message_for_encryption, encryption_type):
    # daca blocul pentru encriptie nu este multiplu de 16 bytes, adaug spatii goale pana la dimensiunea potrivita
    if type(message_for_encryption) is str:
        message_for_encryption = message_for_encryption.encode("utf8")
    block_to_pad = (16 - len(message_for_encryption) % 16) % 16
    message_for_encryption += chr(0).encode("utf8") * block_to_pad
    # apoi codez blocul cu dimensiunea corecta
    iv = Random.new().read(AES.block_size)
    if encryption_type == "CBC":
        aes = AES.new(key_code, AES.MODE_CBC, iv)
    else:
        aes = AES.new(key_code, AES.MODE_ECB, iv)
    send_message = aes.encrypt(message_for_encryption)
    # returnez mesajul format din iv si mesajul proproiu-zis
    return iv + send_message
