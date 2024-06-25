import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

class Encryption:
    @staticmethod
    def pad(s):
        # Padding to make the input a multiple of 16 bytes
        return s + (AES.block_size - len(s) % AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)

    @staticmethod
    def unpad(s):
        # Unpadding the input
        return s[:-ord(s[len(s)-1:])]

    @staticmethod
    def encrypt(plain_text, key):
        # Generating a random IV (Initialization Vector)
        iv = os.urandom(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_text = cipher.encrypt(Encryption.pad(plain_text).encode('utf-8'))
        # Encode to base64 to get a string format
        return base64.b64encode(iv + encrypted_text).decode('utf-8')

    @staticmethod
    def decrypt(encrypted_text, key):
        # Decode the base64 encoded string
        encrypted_text_bytes = base64.b64decode(encrypted_text)
        iv = encrypted_text_bytes[:16]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_text = cipher.decrypt(encrypted_text_bytes[16:])
        return Encryption.unpad(decrypted_text.decode('utf-8'))

    @staticmethod
    def encrypt_data(data):
        key = open("secret.key", "rb").read()
        return Encryption.encrypt(data, key)

    @staticmethod
    def decrypt_data(data):
        key = open("secret.key", "rb").read()
        return Encryption.decrypt(data, key)

