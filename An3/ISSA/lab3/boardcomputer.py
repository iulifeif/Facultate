import json
import socket


def read_json(file_name):
    with open(file_name, "r") as f:
        input_json = f.read()
    return json.loads(input_json)


if __name__ == '__main__':
    content = read_json("boardcomputer.json")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(("localhost", 5000))
        s.sendall(b"boardcomputer")
        message_received = int(s.recv(1024))
        if not message_received:
            s.sendall(str(content["km"]).encode())
        else:
            s.sendall(str(content["avgspeed"]).encode())
