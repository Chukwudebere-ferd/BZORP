from cryptography.fernet import Fernet
from app.core.config import settings


def _get_fernet_key() -> bytes:
    key = settings.secret_key
    if not key:
        return Fernet.generate_key()
    try:
        Fernet(key.encode())
        return key.encode()
    except (ValueError, AttributeError):
        return Fernet.generate_key()


def encrypt_token(token: str) -> str:
    cipher = Fernet(_get_fernet_key())
    return cipher.encrypt(token.encode()).decode()


def decrypt_token(encrypted: str) -> str:
    cipher = Fernet(_get_fernet_key())
    return cipher.decrypt(encrypted.encode()).decode()
