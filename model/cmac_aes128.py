# from Crypto.Hash import CMAC
# from Crypto.Cipher import AES
# from binascii import hexlify, unhexlify
# secret = unhexlify('00'*16)
# message = unhexlify('6bc1bee22e409f96e93d7e117393172a')
# c = CMAC.new(secret,message,ciphermod = AES)
# print(c.hexdigest())

from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from binascii import hexlify, unhexlify
def cmac_aes128(data):
    secret = unhexlify('2b7e151628aed2a6abf7158809cf4f3c')
    message = unhexlify(data)
    print(secret,'\n',message)
    c = CMAC.new(secret,message,ciphermod = AES)
    return c.hexdigest()
# print(cmac_aes128(0))