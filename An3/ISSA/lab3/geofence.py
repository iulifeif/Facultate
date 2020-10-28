import json
import socket
import time

state = False
coords = None


def read_json(file_name):
    with open(file_name, "r") as f:
        input_json = f.read()
    return json.loads(input_json)


if __name__ == '__main__':
    content = read_json("geofence.json")
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("localhost", 5000))
            s.sendall(b"geofence")
            message = s.recv(1024).decode()
            print(message)
            command = json.loads(message)
            if command["command"] == "set_coords":
                coords = command["data"]
                s.sendall(b"OK")
            elif command["command"] == "set_status":
                if coords is None:
                    s.sendall(b"Geofence coordinates not set")
                else:
                    state = command["data"]
                    if state:
                        if coords[0]["latitude"] <= content["latitude"] <= coords[1]["latitude"] and \
                                coords[0]["longitude"] <= content["longitude"] <= coords[1]["longitude"]:
                            s.sendall(b"In bounds")
                        else:
                            s.sendall(b"Out of bounds")
                    else:
                        s.sendall(b"Disabled geofence")
        time.sleep(1)
