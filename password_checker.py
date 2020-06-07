import itertools
import json
import datetime
import operator
import os

class PasswordChecker:
    def __init__(self, client):
        self.client = client
        self.a_to_z = [chr(letter) for letter in range(97, 123)]
        self.zero_to_9 = [chr(letter) for letter in range(48, 58)]
        self.A_to_Z = [chr(letter) for letter in range(65, 91)]


    def password_generator(self):
        length = 1
        while True:
            for pswrd in itertools.combinations(itertools.chain(self.a_to_z, self.zero_to_9), length):
                yield ''.join(pswrd)
            length += 1


    def __check_logins(self):
        with open(os.path.abspath('logins.txt'), 'r') as logins:
            for login in logins:
                self.client.send_message(json.dumps({
                    'login': login.rstrip('\n'),
                    'password': ' '
                }))
                self.client.get_response()
                json_response = json.loads(self.client.server_response)
                if json_response['result'] == 'Wrong password!':
                    return login


    def check_logins_with_passwords(self):
        login = self.__check_logins()
        max_pass_length = 30
        password = ['' for _i in range(max_pass_length)]
        for index in range(max_pass_length):
            password_time_dict = {}
            for letter in itertools.chain(self.a_to_z, self.A_to_Z, self.zero_to_9):
                password[index] = letter
                credentials = {
                    'login': login.rstrip('\n'),
                    'password': ''.join(password)
                }
                credentials = json.dumps(credentials)
                time_before_sending_message = datetime.datetime.now()
                self.client.send_message(credentials)
                self.client.get_response()
                time_after_receiving_message = datetime.datetime.now()
                password_time_dict[letter] = time_after_receiving_message - time_before_sending_message
                json_response = json.loads(self.client.server_response)
                if json_response['result'] == 'Connection success!':
                    return credentials
            password[index] = max(password_time_dict.items(), key=operator.itemgetter(1))[0]


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
                    self.client.send_message(pswrd)
                    self.client.get_response()
                    if self.client.server_response == 'Connection success!':
                        return pswrd


    def crack_password(self):
        return self.check_logins_with_passwords()

        # standard_pass = self.check_standard_passwords()
        # if standard_pass:
        #     return standard_pass


        # attempts = 1
        # generator = self.password_generator()
        # while attempts < 1000000:
        #     password = next(generator)
        #     self.send_message(password)
        #     self.get_response()
        #     if self.server_response == 'Connection success!':
        #         return password
        #     attempts += 1



