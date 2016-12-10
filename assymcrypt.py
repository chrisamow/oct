# PyCrypto https://www.dlitz.net/software/pycrypto/api/2.6/

from Crypto import Random
from Crypto.PublicKey import RSA
import base64



def generate_keys():
    # RSA modulus length must be a multiple of 256 and >= 1024
    modulus_length = 256*4 # use larger value in production
    privatekey = RSA.generate(modulus_length, Random.new().read)
    publickey = privatekey.publickey()
    return privatekey, publickey


def encrypt_message(a_message , publickey):
    encrypted_msg = publickey.encrypt(a_message, 32)[0]
    encoded_encrypted_msg = base64.b64encode(encrypted_msg) # base64 encoded strings are database friendly
    return encoded_encrypted_msg


def decrypt_message(encoded_encrypted_msg, privatekey):
    decoded_encrypted_msg = base64.b64decode(encoded_encrypted_msg)
    decoded_decrypted_msg = privatekey.decrypt(decoded_encrypted_msg)
    return decoded_decrypted_msg


def generate_keyfiles():
    """
    https://www.dlitz.net/software/pycrypto/api/current/Crypto.PublicKey.RSA-module.html
    the library must have changed the exportKey now belongs to the class

    We will use these as the ongoing keys for the database security
    """
    priv, pub = generate_keys()
    with open('key.pem', 'w') as privfile:
        privfile.write(priv.exportKey('PEM'))
    with open('key-public.pem', 'w') as pubfile:
        pubfile.write(pub.exportKey('PEM'))

    #test before we leave
    with open('key.pem','r') as f:
        RSA.importKey(f.read())
    with open('key-public.pem','r') as f:
        RSA.importKey(f.read())


class Crypt(object):
    def __init__(self):
        with open('key.pem','r') as f:
            self.privkey = RSA.importKey(f.read())
        with open('key-public.pem','r') as f:
            self.pubkey = RSA.importKey(f.read())

    def en(self, text):
        #sad last minute hack - Crypto does not support unicode?!!
        if(isinstance(text, unicode)):
            text = text.encode('ascii', 'ignore')
        return encrypt_message(text, self.pubkey)

    def de(self, text):
        return decrypt_message(text, self.privkey)


if __name__ == '__main__':
    warn = raw_input('WARNING: overwriting the key files, type "ok" to continue: ')
    if warn == 'ok':
        generate_keyfiles()
