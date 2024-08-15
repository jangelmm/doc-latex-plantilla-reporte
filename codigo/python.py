import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import zipfile

def encrypt_file(file_path, password):
    # Read the file data
    with open(file_path, 'rb') as f:
        data = f.read()

    # Generate a random salt
    salt = os.urandom(16)
    # Generate a random nonce
    nonce = os.urandom(12)

    # Derive the key from the password
    backend = default_backend()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=backend
    )
    key = kdf.derive(password.encode())

    # Encrypt the data
    aesgcm = AESGCM(key)
    encrypted_data = aesgcm.encrypt(nonce, data, None)

    # Combine salt, nonce, and encrypted data
    encrypted_file_data = salt + nonce + encrypted_data

    # Save the encrypted file
    encrypted_file_path = file_path + '.enc'
    with open(encrypted_file_path, 'wb') as f:
        f.write(encrypted_file_data)

# Uso
file_path = '/home/jangel/Documents/Programming/Python/pro-projects/encriptar-archivos/archivo.txt'
password = '1234567890'

encrypt_file(file_path, password)
