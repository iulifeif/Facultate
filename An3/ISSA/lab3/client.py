import json
import socket


def read_json(file_name):
    with open(file_name, "r") as f:
        input_json = f.read()
    return json.loads(input_json)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 5000))
        s.sendall(b"a")
        message_received = s.recv(1024)
        print(message_received)
