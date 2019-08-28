import hashlib
import webbrowser


print('The following secure hashes/message digests are supported on this platform:')
print(hashlib.algorithms_available)

hashValue = input('Enter a Value to hash: ')

print('\nThe MD5 hash of {} is: '.format(hashValue))
hashObj = hashlib.md5()     # instantiate the hash object for md5
hashObj.update(hashValue)   # add the string to the hashObject instance
print(hashObj.hexdigest())

print('\nusing sha1:')
hashObj = hashlib.sha1()    # instantiate the hash object for sha1
hashObj.update(hashValue)   # add the string to the hashObject instance
print(hashObj.hexdigest())

print('\nusing sha224:')
hashObj = hashlib.sha224()    # instantiate the hash object for sha224
hashObj.update(hashValue)   # add the string to the hashObject instance
print(hashObj.hexdigest())

print('\nusing sha256:')
hashObj = hashlib.sha256()    # instantiate the hash object for sha256
hashObj.update(hashValue)   # add the string to the hashObject instance
print(hashObj.hexdigest())

print('\nusing sha384:')
hashObj = hashlib.sha384()    # instantiate the hash object for sha384
hashObj.update(hashValue)   # add the string to the hashObject instance
print(hashObj.hexdigest())

print('\nusing sha512:')
hashObj = hashlib.sha512()    # instantiate the hash object for sha512
hashObj.update(hashValue)   # add the string to the hashObject instance
print(hashObj.hexdigest())
