from cryptography.fernet import Fernet
import os

class Encryption:
    _FERNET_TOKEN = None

    @staticmethod
    def generate_key():
        """
        Generates a new Fernet key and saves it to a file.
        """
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        print(f"New key generated and saved: {key}")

    @staticmethod
    def load_fernet_token():
        """
        Loads the Fernet token from the file.
        """
        if Encryption._FERNET_TOKEN is None:
            with open("secret.key", "rb") as token:
                Encryption._FERNET_TOKEN = token.read()
        print(f"Token loaded: {Encryption._FERNET_TOKEN}")

    @classmethod
    def encrypt_data(cls, data):
        """
        Encrypts the given data using the cipher suite.

        Args:
            data (str): The data to be encrypted.

        Returns:
            bytes: The encrypted data.
        """
        if cls._FERNET_TOKEN is None:
            cls.load_fernet_token()
        print(f"Token used for encryption: {cls._FERNET_TOKEN}")
        return Fernet(cls._FERNET_TOKEN).encrypt(data.encode())

    @classmethod
    def decrypt_data(cls, encrypted_data):
        """
        Decrypts the given encrypted data using the cipher suite.

        Args:
            encrypted_data (bytes): The data to be decrypted.

        Returns:
            str: The decrypted data.
        """
        if cls._FERNET_TOKEN is None:
            cls.load_fernet_token()
        print(f"Token used for decryption: {cls._FERNET_TOKEN}")
        return Fernet(cls._FERNET_TOKEN).decrypt(encrypted_data).decode()

