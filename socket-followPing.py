import os

while True:

    hostName = input('Enter a FQDN of a website to ping: ')
    if os.name == 'nt':
        response = os.system('ping ' + hostName) # see if it is alive
    else:
        if os.name == 'posix':
            print('Capturing ping to file, be sure to CTRL + BREAK to stop')
            # Execute command (a string):
            response = os.system('ping -c 4 ' + hostName + '>pingFile.txt')

            # and then check the response...

    if os.name == 'nt':
        if response == 0:
            print(hostName, ' is responding!')
        else:
            print(hostName, ' is down!')

    yorn = input('Continue ping? y or n: ')
    if yorn.lower() == 'n':
        break


"""TRY to connect into one of the range of PORTs:
for port in range(52, 500):
    try:
        result = sock.connect((host, port))
        print('\n\tTCP Port {}:\tOpen'.format(port))
        print('\n\tTCP Port Service is: {}\n'.format(socket.getservbyport(port)))
        sock.close()
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
    except:
        print('\r+')
"""
