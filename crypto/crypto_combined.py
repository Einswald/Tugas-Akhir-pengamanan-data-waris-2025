from Crypto.Cipher import AES, Blowfish
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from hashlib import sha256

def encrypt_combined(plain_data, custom_key):
    
    aes_key = sha256(custom_key + b'_aes').digest()[:24]
    blowfish_key = sha256(custom_key + b'_blowfish').digest()[:16]
    
    aes_iv = get_random_bytes(16)
    aes_cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    aes_encrypted = aes_cipher.encrypt(pad(plain_data, AES.block_size))

    blowfish_iv = get_random_bytes(8)
    blowfish_cipher = Blowfish.new(blowfish_key, Blowfish.MODE_CBC, blowfish_iv)
    blowfish_encrypted = blowfish_cipher.encrypt(pad(aes_encrypted, Blowfish.block_size))
    
    return aes_iv + blowfish_iv + blowfish_encrypted


def decrypt_combined(encrypted_data, custom_key):

    aes_key = sha256(custom_key + b'_aes').digest()[:24]
    blowfish_key = sha256(custom_key + b'_blowfish').digest()[:16]

    aes_iv = encrypted_data[:16]
    blowfish_iv = encrypted_data[16:24]
    ciphertext = encrypted_data[24:]

    blowfish_cipher = Blowfish.new(blowfish_key, Blowfish.MODE_CBC, blowfish_iv)
    decrypted_aes_data = unpad(blowfish_cipher.decrypt(ciphertext), Blowfish.block_size)

    aes_cipher = AES.new(aes_key, AES.MODE_CBC, aes_iv)
    final_decrypted = unpad(aes_cipher.decrypt(decrypted_aes_data), AES.block_size)

    return final_decrypted

