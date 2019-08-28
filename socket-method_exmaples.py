import socket


# Test to see if I have an IPv6 stack:
if socket.has_ipv6:
    print('This host supports the IPv6 stack')
else:
    print('This host doesn\'t support IPv6')

hostName = socket.gethostname()
print('This machine name is: ', hostName)

hostFQDN = socket.getfqdn(hostName)
print('This machine Fully Qualified Domain Name: ', hostFQDN)

# The following works IPv4 only:
hostAddr = socket.gethostbyname(hostName)
print(f'The IPv4 Address for machine {hostName}: {hostAddr}')

# Retrieve extended IP address information for this machine:
'''primary host name, alias for that IP, address list of v4 for the same interface.'''
hostAddr = socket.gethostbyname_ex(hostName)
print('\nExtended address information for {}:\n {}'.format(hostName, hostAddr))

# Retrieve it again, but print individual values:
hostname, aliases, addresses = socket.gethostbyname_ex(hostName)
print('\tHost Name (fqdn): ', hostname)
print('\tAlias: ', aliases)
print('\tThis host has {} addresses'.format(len(addresses))) # how many IP addrs
print('\tAddresses: ', addresses)

print('\nThis info refers to ONE adapter\n')

# Determine the IP address by name of another machine:
findHost = input('\nEnter a FQDN to locate: ')
foundHost = socket.gethostbyname(findHost)
print(f'{findHost} has an IP address of: {foundHost}')

ipAddr = input('\nEnter the IP address just found: ')

hostname, aliases, addresses = socket.gethostbyaddr(ipAddr)
print('\tHost Name (fqdn): ', hostname)
print('\tAlias: ', aliases)
print('\tThis host has {} addresses'.format(len(addresses)))
print('\tAddresses: ', addresses)
