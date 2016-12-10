from Crypto import Random
from Crypto.PublicKey import RSA
import base64
import os.path

from .. assymcrypt import generate_keys, encrypt_message, decrypt_message



def est_crypt():
    privatekey , publickey = generate_keys()
    with open('tests/givingtree.txt','r') as myfile:    #assumes we are py.test from parent dir
        lines = myfile.readlines()
        for txt in lines:
            encrypted_msg = encrypt_message(txt , publickey)
            decrypted_msg = decrypt_message(encrypted_msg, privatekey)
            #print ("{} - {}".format(privatekey.exportKey() , len(privatekey.exportKey())) )
            #print ("{} - {}".format(publickey.exportKey() , len(publickey.exportKey())) )
            #print (" Original content: {} - {}".format(txt, len(txt)) )
            #print ("Encrypted message: {} - {}".format(encrypted_msg, len(encrypted_msg)) )
            #print ("Decrypted message: {} - {}".format(decrypted_msg, len(decrypted_msg)) )
            assert txt == decrypted_msg



def test_keyfiles():
    assert os.path.exists('key.pem')
    assert os.path.exists('key-public.pem')

    priv, pub = None, None
    with open('key.pem','r') as f:
        priv = RSA.importKey(f.read())
    with open('key-public.pem','r') as f:
        pub = RSA.importKey(f.read())

    txt = 'The keys should work even after export import'
    encrypted_msg = encrypt_message(txt , pub)
    decrypted_msg = decrypt_message(encrypted_msg, priv)
    assert txt == decrypted_msg


if __name__ == '__main__':
    test_keyfiles()

