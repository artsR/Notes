import socket
import sys


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Create a TCP/IP socket
#sock.bind()   # : Binds address (hostname, port number) to socket
#sock.listen() # : Sets up and starts TCP listener
#sock.accept() # : Accepts TCP client connection

# Define host and communication port:
host = 'localhost'
port = 8080

sock.bind((host, port))
sock.listen(1) # listen for incoming connections

# Wait for a connection
print('Waiting for a connection')
connection, client = sock.accept()
print(client, 'connected')

# Receive the data in small chunks and retransmit it:
data = connection.recv(16)
print('received "%s"' % (data) )
if data:
  connection.sendall(data)
 else:
  print('No data from', client)
 
 # Close the connection:
 connection.close()
