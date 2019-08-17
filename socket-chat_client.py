import socket
import select  # https://pymotw.com/2/select/ # waiting for I/O
""" ^ Polling is the process where the computer or controlling device waits for
an external device to check for its readiness or state"""
import sys, time


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) != 3:
    print('Correct usage: script, IP address, port number')
    exit()
hostname = str(sys.argv[1])
port = int(sys.argv[2])

# Try to get IP by hostname:
try:
    ip_address = socket.gethostbyname(hostname)
except:
    print('Hostname could not be resolved.')
    pass
server.connect((ip_address, port)) # Or server.connect((remote_ip, port))

"""if the socket is running in blocking mode (which is the default).
You tell it to read, and it waits until new data arrives."""
# To prevent it set connection to non-blocking state:
server.setblocking(0)

while True:
    # Maintain a list of possible input streams:
    #sockets_list = [sys.stdin, server]

    """There are 2 possible input situations.
    Either the user wants to give manual input to send to other people, or
    the server is sending a message to be printed on the screen.
    Select returns from 'sockets_list' the stream that is reader for input.
    So for example, if the server wants to send a message,
    the else condition will be evaluated as true."""
    # read_sockets, write_socket, error_socket = select.select(sockets_list, [], []) # stops here
    print('p2')
    try:
        while True:
            print('p3')
            username_header = server.recv(3)
            print('p4')
            if not len(username_header):
                print('Conncetion terminated by the server')
                sys.exit()
            print('p5')
            message = server.recv(1024).decode('utf-8')
            print('p6')
            print(message)
            #-------------------------
            time.sleep(2)
            message = input('> ')
            if message:
                print('p7')
                message = bytes(message, 'utf-8')
                server.send(message)
            #------------------------
    except IOError as e:
        continue
    print('p8')
    # for socks in read_sockets:
    #     print('In for')
    #     if socks == server:
    #         message = socks.recv(2048)
    #         print(message.decode("utf-8"))
    #     else:
    #         message = sys.stdin.readline()
    #         server.send(message)
    #         sys.stdout.write("<ME>")
    #         sys.stdout.write(message.decode("utf-8"))
    #         sys.stdout.flush()
            # https://www.binarytides.com/code-chat-application-server-client-sockets-python/
			# Data recieved from client, process it
            # try:
			# 	#In Windows, sometimes when a TCP program closes abruptly,
			# 	# a "Connection reset by peer" exception will be thrown
            #     data = socks.recv(2048)
            #     if data:
            #         broadcast(sock, "\r" + '<' + str(socks.getpeername()) + '> ' + data)
			# except:
            #     broadcast("Client (%s, %s) is offline" % addr, socks)
            #     print("Client (%s, %s) is offline" % addr)
            #     socks.close()
            #     sockets_list.remove(socks)
            #     continue
            # """If anyone wonders why the server does not handle a client disconnect properly:
            # just move or copy the lines 60-64 from “except” block up to the “if – else” block.
            #
            # if data:
            #     broadcast_data(sock, “\r” + ‘ ‘ + data)
            # else:
            # broadcast_data(sock, “Client (%s, %s) is offline” % addr)
            # print “Client (%s, %s) is offline” % addr
            # sock.close()
            # CONNECTION_LIST.remove(sock)
            # continue """

server.close()
