import os
import json
from cryptography.fernet import Fernet

class MediaVault:
    def __init__(self, key):
        self.key = key
        self.vault = {}

    def load_vault(self):
        try:
            with open('vault.json', 'r') as file:
                encrypted_data = file.read()
                decrypted_data = self.decrypt_data(encrypted_data)
                self.vault = json.loads(decrypted_data)
        except FileNotFoundError:
            pass

    def save_vault(self):
        with open('vault.json', 'w') as file:
            json_data = json.dumps(self.vault)
            encrypted_data = self.encrypt_data(json_data)
            file.write(encrypted_data)

    def encrypt_data(self, data):
        cipher_suite = Fernet(self.key)
        encrypted_data = cipher_suite.encrypt(data.encode())
        return encrypted_data.decode()

    def decrypt_data(self, encrypted_data):
        cipher_suite = Fernet(self.key)
        decrypted_data = cipher_suite.decrypt(encrypted_data.encode())
        return decrypted_data.decode()

    def add_media(self, file_path, media_type):
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                media_data = file.read()
                self.vault[os.path.basename(file_path)] = {'type': media_type, 'data': media_data}
                self.save_vault()

    def get_media(self, file_name):
        return self.vault.get(file_name, None)

    def remove_media(self, file_name):
        if file_name in self.vault:
            del self.vault[file_name]
            self.save_vault()


# Example usage:
if __name__ == "__main__":
    key = Fernet.generate_key()
    vault = MediaVault(key)

    # Load existing vault if available
    vault.load_vault()

    # Add media files
    vault.add_media('example_image.jpg', 'image')
    vault.add_media('example_video.mp4', 'video')

    # Get media
    print(vault.get_media('example_image.jpg'))
    print(vault.get_media('example_video.mp4'))

    # Remove media
    vault.remove_media('example_image.jpg')

    # Save vault
    vault.save_vault()
