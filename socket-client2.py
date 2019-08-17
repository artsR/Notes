import socket
import pickle

HEADER_SIZE = 10
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 500
server.connect((host, port))


while True:
    ful_msg = b''
    recv_msg = True
    while True:
        msg = server.recv(5)
        if recv_msg:
            print(f'The length of message = {msg[:HEADER_SIZE]}')
            x = int(msg[:HEADER_SIZE])
            recv_msg = False
        ful_msg += msg
        if len(ful_msg)-HEADER_SIZE == x:
            print('Received the complete message')
            print(ful_msg[HEADER_SIZE])
            data = pickle.loads(ful_msg[HEADER_SIZE:])
            print(data)
            recv_msg = True
            ful_msg = b''
print(ful_msg)


print(pickle.loads(ful_msg))
