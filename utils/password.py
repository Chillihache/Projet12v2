from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError


ph = PasswordHasher()


def set_password(password):
    return ph.hash(password)


def verify_password(password, hashed_password):
    try:
        return ph.verify(hashed_password, password)
    except VerifyMismatchError:
        return False
