import socket

from Crypto.Cipher import AES

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 5000       # Port to listen on (non-privileged ports are > 1023)


if __name__ == '__main__':
    K3 = "4h8f.093mJo:*9#$"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 5000))
        s.listen()
        conn, addr = s.accept()
        with conn:
            while True:
                # primeste mesajul de la A
                received_message = conn.recv(1024).decode()
                print("[B]Am primit de la nodul A mesajul: " + received_message)
                # ia legatura cu nodul KM pentru a-i cere cheia speciala
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_KM:
                    socket_KM.connect(("0.0.0.0", 5005))
                    # ii trimite lui KM modul de criptare primit de la A
                    socket_KM.sendall(received_message.encode())
                    print("[A] Am trimis catre KM " + received_message)
                    # primeste de la KM cheia
                    # iv, received_message = socket_KM.recv().decode()
                    received_message = socket_KM.recv(1024)
                    iv = received_message[:16]
                    aes = AES.new(K3, AES.MODE_CBC, iv)
                    key_decode = aes.decrypt(received_message[16:])
                    print("[A] Am primit de la KM mesajul: " + key_decode)
