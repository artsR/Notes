import socket
import sys
from threading import *


"""The first argument AF_INET is the address domain of the socket.
INET: IPv4; other possibilities: AF_INET6, AF_BLUETOOTH, AF_UNIX...
This is used when we have an Internet Domain with any two hosts.
The second argument is the type of socket. SOCK_STREAM means that data
or characters are read in a continuous flow (TCP). """
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

"""Prevents the 'Address already in use'
that we hit often while building our programs"""
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Check whether sufficient arguments have been provided:
"""$python chat_server.py server_IP port"""
if len(sys.argv) != 3:
    print('Correct usage: script, IP address, port number')
    exit()

# Take the first argument from command prompt as IP address:
IP_address = str(sys.argv[1])

# Take the second argument as port number:
PORT = int(sys.argv[2])

"""Binds the Server to an entered IP and at the specified port number.
It means that Server informs Operating System about it.
The Client must be aware of these parameters."""
server.bind((IP_address, PORT))

'''Listens for 100 active connections.'''
server.listen(10)

list_of_clients = []

#-------------------------------------------------------------------------------
def clientThread(conn, addr):

    # Send a message to the client whose user object is 'conn':
    conn.send('Welcome to this chatroom, sir!'.encode('utf-8'))
    while True:
        try:
            message = conn.recv(2048)
            if message:
                """Prints the message and address of the user who just sent the
                message on the server terminal"""
                print("<" + addr[0] + ">" + message)

                # Call broadcast function to send message to all:
                message_to_send = "<" + addr[0] + ">" + message
                broadcast(message_to_send, conn)
            else:
                """Message may have no content if the connection is broken,
                in this case removes the connection."""
                remove(conn)
        except:
            continue

def broadcast(message, connection):
    """Using this function to broadcast the message to all clients who's object
    is not the same as the one sending message."""
    for client in list_of_clients:
        if client != connection:
            try:
                client.send(message.encode('utf-8'))
                #Or client.send(bytes(message, "utf-8"))
            except:
                client.close()
                """If the link is broken, removes the client."""
                remove(client) # or list_of_clients.remove(client) - because it's a list

def remove(connection):
    """Removes the object (client) from the list that was created
    at the beginning of the program."""
    if connection in list_of_clients:
        list_of_clients.remove(connection)
#-------------------------------------------------------------------------------
while True:
    print(f'Listening for connections on {IP_address}:{PORT}...')
    """Accepts a connection request and stores two parameters:
    'conn' which is a socket object for that user, and
    'addr' which is the IP address of the client """
    conn, addr = server.accept()

    """Maintains a list of clients for ease of broadcasting a message
    to all available people in the chatroom"""
    list_of_clients.append(conn)

    # Print the address of the user that just connected:
    print(addr, " connected")

    # Creates an individual thread for every user
    # that connects:
    Thread(target=clientThread, args=(conn, addr)).start()

conn.close() # co powstrzymuje dojscie do tego momentu ?? Anw: server.accept()
print('Client disconnected')
server.close()
print('Server closed.')
