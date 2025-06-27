import hashlib

SALT = "your_salt_here"

def encrypt_password(password: str) -> str:
    return hashlib.md5((SALT + password).encode('utf-8')).hexdigest()
