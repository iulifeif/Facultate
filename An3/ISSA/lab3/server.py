import json
from socketserver import BaseRequestHandler, TCPServer


class MessageHandler(BaseRequestHandler):
    def handle(self) -> None:
        message_received = self.request.recv(1024)
        if message_received == b"boardcomputer":
            request = input("Boardcomputer request option: ")
            self.request.send(request.encode())
            print(self.request.recv(1024))
        elif message_received == b"geofence":
            request = input("Geofence request [enable/disable/coords]: ")
            if request == "enable":
                self.request.send(json.dumps({
                    "command": "set_status",
                    "data": True
                }).encode())
            elif request == "disable":
                self.request.send(json.dumps({
                    "command": "set_status",
                    "data": False
                }).encode())
            elif request == "coords":
                coords = [
                    {"latitude": float(input("Latitude #1:")),
                     "longitude": float(input("Longitude #1:"))},
                    {"latitude": float(input("Latitude #2:")),
                     "longitude": float(input("Longitude #2:"))}
                ]
                self.request.send(json.dumps({
                    "command": "set_coords",
                    "data": coords
                }).encode())
            print(self.request.recv(1024))


if __name__ == '__main__':
    server = TCPServer(("0.0.0.0", 5000), MessageHandler)
    try:
        server.serve_forever()
    except BaseException:
        server.shutdown()
        raise
