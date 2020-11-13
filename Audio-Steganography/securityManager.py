import base64
import os
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import bitarray as ba
from cryptography.fernet import Fernet


def getKey(password_provided):
    password = password_provided.encode()
    salt = b'salt_'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key


def encrypt(f, password_provided):
    key = getKey(password_provided)
    data = f.read()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)
    lol = ba.bitarray()
    lol.frombytes(encrypted)
    return lol


def decrypt(msgBits, password_provided):
    data = msgBits.tobytes()
    key = getKey(password_provided)
    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    return decrypted
