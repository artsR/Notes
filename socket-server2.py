import socket
import pickle, time

HEADER_SIZE = 10
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostname()
port = 500
server.bind((host, port))
server.listen(10)

data = {'Mercedes CLS': 100350, 'Audi A4':98000, 'BMW': 79000}

# Pickle data:
"""The data will be serialized with 'pickle'. Serialization is
the conversion of my object to 'bytes'"""
msg = pickle.dumps(data)
msg = bytes(f'{len(msg):<{HEADER_SIZE}}','utf-8') + msg

while True:
    conn, addr = server.accept()
    print(f'Connection to {addr} established')
    #conn.send(bytes('Welcome to our server', 'utf-8'))
    conn.send(msg) # the sent data must be bytes
    #------ some fancy code ------------
    while True:
        time.sleep(3)
        msg = f'{time.time()}'
        msg = pickle.dumps(msg)
        msg = bytes(f'{len(msg):<{HEADER_SIZE}}','utf-8') + msg
        conn.send(msg)
    #-----------------------------------
    conn.close()
    print(f'Client {addr} disconnected')
