import socket
from Cryptodome import Random
from Cryptodome.Cipher import AES


class Crypto:
    def __init__(self, key_code, iv=0):
        if not iv:
            self.iv = Random.new().read(AES.block_size)
        else:
            self.iv = iv
        self.key_code = key_code


class Decrytor (Crypto):
    def decrypt_message(self, message_for_decryption, type_crypt):
        buffer_text = b""
        self.iv = message_for_decryption[:16]
        for index_block in range(16, len(message_for_decryption), 16):
            block_message = message_for_decryption[index_block:index_block + 16]
            saved_block_message = block_message
            aes = AES.new(self.key_code, AES.MODE_ECB)
            decrypted_block = aes.decrypt(block_message)
            if type_crypt == "CBC":
                decrypted_block = byte_xor(decrypted_block, self.iv)
                self.iv = saved_block_message
            buffer_text += decrypted_block
        return buffer_text.strip(chr(0).encode("utf8"))


class Encryptor(Crypto):
    def encrypt_message(self, message_for_encryption, type_crypt):
        buffer_text = self.iv
        message_for_encryption = str_to_byt(message_for_encryption)
        message_for_encryption = pad(message_for_encryption)
        for index_block in range(0, len(message_for_encryption), 16):
            block_message = message_for_encryption[index_block:index_block + 16]
            aes = AES.new(self.key_code, AES.MODE_ECB)
            if type_crypt == "CBC":
                block_message = byte_xor(block_message, self.iv)
            self.iv = aes.encrypt(block_message)
            buffer_text += self.iv
        # returnez mesajul proproiu-zis
        return buffer_text


def byte_xor(ba1, ba2):
    return bytes(a ^ b for a, b in zip(ba1, ba2))


def get_key_from_KM(K3, encryption_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_KM:
        # se conteaza la portul 5005 unde este KM
        socket_KM.connect(("0.0.0.0", 5005))
        # ii trimite lui KM modul de criptare ales
        socket_KM.sendall(encryption_type.encode())
        # primeste de la KM cheia impreuna cu iv
        message_key = socket_KM.recv(1024)
    # ii face decode pentru a fi de tip string cheia de la KM
    decrypt = Decrytor(K3)
    return decrypt.decrypt_message(message_key, encryption_type)


def pad(text_to_pad):
    # daca blocul pentru encriptie nu este multiplu de 16 bytes, adaug spatii goale pana la dimensiunea potrivita
    blocks = (16 - len(text_to_pad) % 16) % 16
    text_to_pad += chr(0).encode("utf8") * blocks
    return text_to_pad


def str_to_byt(input):
    if type(input) is str:
        return input.encode("utf8")
    return input

