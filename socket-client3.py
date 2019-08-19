import socket


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
IP   = socket.gethostbyname(HOST)
PORT = 8080

client.connect((IP, PORT))
client.setblocking(False) # socket.recv() doesn't block executing code
client.settimeout(10)     # accepts up to 10 seconds of silence from server

while True:
    message = client.recv(1024)
    print(message.decode('utf-8'))
