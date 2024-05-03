from cryptography.fernet import Fernet


class Encryptor:
    """
    A class for encrypting and decrypting data using the Fernet symmetric encryption algorithm.

    Attributes:
        - cipher (Fernet): The Fernet cipher object used for encryption and decryption.

    Methods:
        - encrypt_data(data: str) -> bytes:
            Encrypts the given string data and returns the encrypted bytes.

        - decrypt_data(encrypted_data: bytes) -> str:
            Decrypts the given encrypted bytes and returns the original string data.

        - check_equivalence(data: str, encrypted_data: bytes) -> bool:
            Checks if the decrypted encrypted data matches the original data,
            returning True if they are equivalent, False otherwise.
    """

    def __init__(self, secret_key):
        self.cipher = Fernet(secret_key)

    def encrypt_data(self, data):
        encrypted_data = self.cipher.encrypt(data.encode("utf-8"))
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.cipher.decrypt(encrypted_data).decode("utf-8")
        return decrypted_data

    def check_equivalence(self, data, encrypted_data):
        return self.decrypt_data(encrypted_data) == data
