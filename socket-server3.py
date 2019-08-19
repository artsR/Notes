import socket
import time
import threading


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

HOST = 'localhost'
IP   = socket.gethostbyname(HOST)
PORT = 8080

server.bind((IP, PORT))
server.listen(5)
print(f'Listening on {IP}:{PORT}...')

def run(server):

    while True:
        message = 'Welcome !'
        client, addr = server.accept()
        print(f'{addr} connected.')
        client.send(message.encode('utf-8'))
        while True:
            time.sleep(5)
            message = f'{time.ctime()}'.encode('utf-8')
            try:
                client.send(message)
            except:
                print(f'{addr} disconnected!')
                break
#----------------------------------------------------------
"""By threading it is possible to shutdown listening and close program in
console, otherwise it hangs.
"""
shutdown_evt = threading.Event()
server_thread = threading.Thread(target=run, args=[server])
server_thread.daemon = True
server_thread.start()
newline = '\n'
input('___________________________________Press enter to shutdown..\n')
shutdown_evt.set()
server.shutdown(socket.SHUT_WR) # I don't know how those arguments work.
#----------------------------------------------------------
