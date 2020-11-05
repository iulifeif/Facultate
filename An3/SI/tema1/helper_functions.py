import socket
from Cryptodome import Random
from Cryptodome.Cipher import AES


# creez o clasa Crypto pentru a salva iv ul si cheia de criptare ce urmeaza sa fie folosita
class Crypto:
    def __init__(self, key_code, iv=0):
        if not iv:
            self.iv = Random.new().read(AES.block_size)
        else:
            self.iv = iv
        self.key_code = key_code


# creez o clasa mostenita din clasa de baza Crypto pentru a cripta mesajele primite
class Encryptor(Crypto):
    def encrypt_message(self, message_for_encryption, type_crypt):
        # prima oara pun in buffer iv-ul pentru ca ne va trebui la decriptare
        buffer_text = self.iv
        # in cazul in care primesc un mesaj str, il convertesc in bytes
        message_for_encryption = str_to_byt(message_for_encryption)
        # padez textul pentru a avea o lungime multiplu de 16
        message_for_encryption = pad(message_for_encryption)
        # iau block uri de cate 16 bytes din text
        for index_block in range(0, len(message_for_encryption), 16):
            # salvez block ul
            block_message = message_for_encryption[index_block:index_block + 16]
            # apelez AES
            aes = AES.new(self.key_code, AES.MODE_ECB)
            # daca criptarea este CBC, voi face si xor
            if type_crypt == "CBC":
                # fac xor intre block ul de mesaj si iv-ul care prima data va fi generat Random
                # iar urmatoarele dati va fi block ul criptat precedent
                block_message = byte_xor(block_message, self.iv)
            # salvez in iv block ul criptat, pentru criptarea urmatorului block
            self.iv = aes.encrypt(block_message)
            # adaug in buffer textul criptat
            buffer_text += self.iv
        # returnez tot mesajul criptat
        return buffer_text


# creez o clasa mostenita din clasa de baza Crypto pentru a decripta mesajele primite
class Decrytor (Crypto):
    def decrypt_message(self, message_for_decryption, type_crypt):
        buffer_text = b""
        # iau primii 16 bytes din mesajul criptat, deoarece aceia sunt iv-ul
        self.iv = message_for_decryption[:16]
        # creez block uri de 16 bytes, de la pozitia 16 incolo, deoarece primii 16 au fost iv-ul
        # pana la finalul lungimii mesajului
        for index_block in range(16, len(message_for_decryption), 16):
            # salvez in block_message bucata de block
            block_message = message_for_decryption[index_block:index_block + 16]
            # mai salvez undeva bucata de block criptat pentru mai tarziu
            saved_block_message = block_message
            # apelez AES
            aes = AES.new(self.key_code, AES.MODE_ECB)
            # decriptez block ul criptat
            decrypted_block = aes.decrypt(block_message)
            # daca modul de criptare este CBC, trebuie sa fac si xor pe block
            if type_crypt == "CBC":
                # fac xor intre block ul decriptat si iv-ul care la inceput este primul block de 16 bytes
                # iar apoi este block ul precedent
                decrypted_block = byte_xor(decrypted_block, self.iv)
                # pun iv block ul criptat salvat mai sus in saved, pentru a fi folosit la decriptarea urmatorului block
                self.iv = saved_block_message
            # adaug in buffer bucata de text decriptata
            buffer_text += decrypted_block
        # iar la final scot toate spatiile puse la final pentru padare si trimit tot textul
        return buffer_text.strip(chr(0).encode("utf8"))


# functia de xor pe doua multimi de bytes, deoarece doua multimi de bytes nu pot fi xor-ate deodata (ca la string)
# trebuie luat byte cu byte si facut xor
def byte_xor(ba1, ba2):
    return bytes(a ^ b for a, b in zip(ba1, ba2))


# functia care cere lui KM cheia pentru modul de encriptie dat
def get_key_from_KM(K3, encryption_type):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_KM:
        # se conteaza la portul 5005 unde este KM
        socket_KM.connect(("0.0.0.0", 5005))
        # ii trimite lui KM modul de criptare primit ca input
        socket_KM.sendall(encryption_type.encode())
        # primeste de la KM cheia impreuna cu iv-ul
        message_key = socket_KM.recv(1024)
    # creeaza o instanta a clasei pentru decodare si ii da cheia K3, pentru ca cu aceasta este codat mesajul
    decrypt = Decrytor(K3)
    # returneaza mesajul decriptat, adica cheia pentru tipul de criptare dat ca si imput
    return decrypt.decrypt_message(message_key, encryption_type)


# functia de padare a unui text, pentru cazul in care textul nu are o lungime multiplu de 16
# altfel nu ii face nimic textului
def pad(text_to_pad):
    # daca blocul pentru encriptie nu este multiplu de 16 bytes, adaug spatii goale pana la dimensiunea potrivita
    blocks = (16 - len(text_to_pad) % 16) % 16
    text_to_pad += chr(0).encode("utf8") * blocks
    return text_to_pad


# functia ce converteste textul primit ca si input din string in bytes
# daca este deja bytes nu il modifica cu nimic
def str_to_byt(input):
    if type(input) is str:
        return input.encode("utf8")
    return input

