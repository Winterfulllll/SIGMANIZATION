from cryptography.fernet import Fernet

class Encryptor:
    def __init__(self, secret_key):
        self.cipher = Fernet(secret_key)

    def encrypt_data(self, data):
        encrypted_data = self.cipher.encrypt(data.encode("utf-8"))
        return encrypted_data

    def decrypt_data(self, encrypted_data):
        decrypted_data = self.cipher.decrypt(encrypted_data).decode("utf-8")
        return decrypted_data

