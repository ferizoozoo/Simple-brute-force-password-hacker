import sys
from password_checker import PasswordChecker
from client import Client

def main():
    ip_address, port = sys.argv[1:3]
    client = Client(ip_address, int(port))
    password_checker = PasswordChecker(client)
    password = password_checker.crack_password()
    print(password)
    client.close_connection()

if __name__ == '__main__':
    main()