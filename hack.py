# write your code here
import sys
import os
import socket
import itertools

a_to_z = [chr(letter) for letter in range(97, 123)]
zero_to_9 = [chr(letter) for letter in range(48, 58)]


def password_generator():
    length = 1
    while True:
        for pswrd in itertools.combinations(itertools.chain(a_to_z, zero_to_9), length):
            yield ''.join(pswrd)
        length += 1


class Client:
    def __init__(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port

        self.socket = socket.socket()
        self.socket.connect((self.ip_address, self.port))


    def check_standard_passwords(self):
        with open(os.path.abspath('passwords.txt'), 'r') as passwords:
            standard_passwords = [password.rstrip('\n') for password in passwords]
            for password in standard_passwords:
                password = password.rstrip('\n')
                for i in itertools.product([0,1], repeat=len(password)):
                    pswrd = ''
                    for j in range(len(i)):
                        if i[j] == 0:
                            pswrd += password[j].upper()
                        else:
                            pswrd += password[j]
                    self.send_message(pswrd)
                    self.get_response()
                    if self.server_response == 'Connection success!':
                        return pswrd


    def crack_password(self):
        standard_pass = self.check_standard_passwords()
        if standard_pass:
            return standard_pass
        # attempts = 1
        # generator = password_generator()
        # while attempts < 1000000:
        #     password = next(generator)
        #     self.send_message(password)
        #     self.get_response()
        #     if self.server_response == 'Connection success!':
        #         return password
        #     attempts += 1

    def send_message(self, message):
        self.socket.send(message.encode('UTF-8'))

    def get_response(self):
        self.server_response = self.socket.recv(1024).decode('UTF-8')

    def close_connection(self):
        self.socket.close()

    def __str__(self):
        return self.server_response


if __name__ == '__main__':
    ip_address, port = sys.argv[1:3]
    client = Client(ip_address, int(port))
    password = client.crack_password()
    print(password)
    client.close_connection()

