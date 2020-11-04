import socket

from Crypto.Cipher import AES

HOST = "0.0.0.0"  # The server's hostname or IP address
PORT = 5000        # The port used by the server


if __name__ == '__main__':
    key_dict = {
        "ECB": "K1",
        "CBC": "K2"
    }
    K3 = "4h8f.093mJo:*9#$"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_b:
        socket_b.connect(("0.0.0.0", 5000))
        type_crypt = input("[A]Ce fel de criptare vrei sa se execute? (ECB/CBC) ")
        # trimite nodului B ce fel de criptare va folosi
        socket_b.sendall(type_crypt.encode())
        print("Voi trimite nodului B mesaju: " + type_crypt)
        # trimite mesaj catre KM sa i dea cheia
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_KM:
            socket_KM.connect(("0.0.0.0", 5005))
            socket_KM.sendall(type_crypt.encode())
            print("[A] Am trimis catre KM " + type_crypt)
            # primeste de la KM cheia
            received_message = socket_KM.recv(1024)
            print("Am primit de la KM", len(received_message), "bytes")
            iv = received_message[:16]
            aes = AES.new(K3, AES.MODE_CBC, iv)
            key_decode = aes.decrypt(received_message[16:])
            print("[A] Am primit de la Km mesajul: ", key_decode)
