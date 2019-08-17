import socket
import pickle

HEADER_SIZE = 10
PACKAGE_SIZE = 16
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 500
server.connect((host, port))

while True:
    ful_msg = b'' # prepared for containing new message
    recv_msg = True
    while True:
        msg = server.recv(PACKAGE_SIZE)
        ful_msg += msg
        if len(msg) == 0:
            break
        # Parse the Header:
        if recv_msg:
            print(f'The length of message = {msg[:HEADER_SIZE]}')
            x = int(msg[:HEADER_SIZE])
            recv_msg = False

        if len(ful_msg)-HEADER_SIZE == x:
            print('Received the complete message')
            print(ful_msg[HEADER_SIZE:])
            data = pickle.loads(ful_msg[HEADER_SIZE:])
            print(data)
            break
