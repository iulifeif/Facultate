import socket

HOST = "0.0.0.0"  # The server's hostname or IP address
PORT = 5000        # The port used by the server


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("0.0.0.0", 5000))
        s.sendall(b'Hello, world')
        data = s.recv(1024)

    print('Received', repr(data))
