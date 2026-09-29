from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError, VerificationError, InvalidHashError

_password_hasher = PasswordHasher()

def hash_password(password: str) -> str :
    return _password_hasher.hash(password)

def verify_password(hashed: str, password : str) -> bool:
    try:
        _password_hasher.verify(hashed, password)
    except(VerifyMismatchError, VerificationError, InvalidHashError):
        return False

def need_rehash(hashed: str) -> bool:
    return _password_hasher.check_needs_rehash(hashed)