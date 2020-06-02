# write your code here
import sys
import socket

class Client:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        self.socket = socket.socket()
        self.socket.connect((self.ip_address, self.port))

    def send_message(self, message):
        self.socket.send(message.encode('UTF-8'))

    def get_response(self):
        self.server_response = self.socket.recv(1024).decode('UTF-8')

    def close_connection(self):
        self.socket.close()

    def __str__(self):
        return self.server_response


if __name__ == '__main__':
    ip_address, port, message = sys.argv[1:4]
    client = Client(ip_address, int(port))
    client.send_message(message)
    client.get_response()
    print(client)
    client.close_connection()

