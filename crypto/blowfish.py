# blowfish.py

from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad, unpad

def encrypt_blowfish(data, key, iv):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    padded_data = pad(data, Blowfish.block_size)
    return cipher.encrypt(padded_data)

def decrypt_blowfish(encrypted_data, key, iv):
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_data), Blowfish.block_size)
    return decrypted
