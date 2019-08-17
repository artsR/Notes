import socket
import pickle

HEADER_SIZE = 10
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 500
server.bind((host, port))
server.listen(10)

data = {'Mercedes CLS': 100350, 'Audi A4':98000, 'BMW': 79000}
msg = pickle.dumps(data)
msg = bytes(f'{len(msg):<{HEADER_SIZE}}','utf-8') + msg

while True:
    conn, addr = server.accept()
    print(f'Connection to {addr} established')
    #conn.send(bytes('Welcome to our server', 'utf-8'))
    conn.send(msg)
    conn.close()
