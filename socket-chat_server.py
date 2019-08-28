#! python3

import socket
import sys
import logging
from threading import *


#logging.disable()
logging.basicConfig(filename='socket-chat_serverLog.txt',
                    level=logging.DEBUG,
                    format=' %(levelname)s- %(message)s')

HEADER_LEN = 10
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
HOST = str(sys.argv[1])
# Take the second argument as port number:
PORT = int(sys.argv[2])
IP   = socket.gethostbyname(HOST)
"""Binds the Server to an entered IP and at the specified port number.
It means that Server informs Operating System about it.
The Client must be aware of these parameters."""
# server.bind((' ',PORT)) # accept from any interface. Any incoming connections
# server.bind(('127.0.0.1',PORT)) # only connect locally
# server.bind(('10.255.88.76',PORT)) # only this specific interface
server.bind((IP, PORT))

'''Listens for 100 active connections.'''
server.listen(10)
logging.debug('Server is ready to listening...')

list_of_clients = []

#-------------------------------------------------------------------------------
def clientThread(conn, addr):
    logging.debug('Start of "clientThread" function')
    # Send a message to the client whose user object is 'conn':
    msg_welcome = 'Welcome to this chatroom, sir!'
    msg_header  = f'{len(msg_welcome):<{HEADER_LEN}}'
    message     = msg_header + msg_welcome
    conn.send(message.encode('utf-8'))
    while True:
        logging.debug('Start of "while" in "clientThread"')
        try:
            logging.debug('"try" to receive message in "clientThread"')
            message = conn.recv(1024)
            logging.debug('message received in "clientThread": ' + str(message))
            if message:
                logging.debug('"if message" in "clientThread"')
                #"""Prints the message and address of the user who just sent the
                #message on the server terminal"""
                print("<" + addr[0] + ">" + message.decode('utf-8'))

                # Call broadcast function to send message to all:
                message_to_send = "<" + addr[0] + ">" + message.decode('utf-8')
                msg_to_send_hdr = f'{len(msg_welcome):<{HEADER_LEN}}'
                message_to_send = msg_to_send_hdr + message_to_send
                broadcast(message_to_send, conn)
            else:
                logging.debug('in "else" in "clientThread"')
                """Message may have no content if the connection is broken,
                in this case removes the connection."""
                remove(conn)
        except IOError as e:
            logging.debug('"except" in "clientThread": ' + str(e))
            continue

def broadcast(message, connection):
    logging.debug('in "broadcast", message_to_send: ' + str(message))
    """Using this function to broadcast the message to all clients who's object
    is not the same as the one sending message."""
    for client in list_of_clients:
        logging.debug('in "for" in "broadcast"')
        if True: #client != connection:
            logging.debug('in "if" in "broadcast"')
            try:
                logging.debug('Trying send message_to_send in "broadcast"')
                client.send(message.encode('utf-8'))
                logging.debug('message_to_send is sent in "broadcast"')
                #Or client.send(bytes(message, "utf-8"))
            except:
                logging.debug('in "except" in "broadcast": ' + str(sys.exc_info()[0]))
                client.close()
                """If the link is broken, removes the client."""
                remove(client) # or list_of_clients.remove(client) - because it's a list

def remove(connection):
    logging.debug('in "remove" function')
    """Removes the object (client) from the list that was created
    at the beginning of the program."""
    if connection in list_of_clients:
        logging.debug('in "if" in "remove"')
        list_of_clients.remove(connection)
#-------------------------------------------------------------------------------
while True:
    print(f'Listening for connections on {IP}:{PORT}...')
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
    logging.debug('after "Thread" in "main while"')
loggin.debug('outside "main while"')
conn.close() # co powstrzymuje dojscie do tego momentu ?? Anw: server.accept()
print('Client disconnected')
server.close()
print('Server closed.')
