from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

# Enkripsi AES dengan key dan IV
def encrypt_aes_cbc(plain_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plain_data, AES.block_size)
    encrypted = cipher.encrypt(padded_data)
    return encrypted

# Dekripsi AES dengan key dan IV
def decrypt_aes_cbc(encrypted_data, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted = unpad(cipher.decrypt(encrypted_data), AES.block_size)
    return decrypted
