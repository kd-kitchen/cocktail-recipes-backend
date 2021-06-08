import hashlib

from .dataclasses import Account


def validate(acc: Account, password: str):
    """
    Checks if the password is valid

    :param acc: The Account instance
    :param password: Input password
    :return: True if password is valid else false
    """
    hashed_password = acc.password
    _, salt = hashed_password.split(':')
    return hashed_password == hash_password(password, salt)


def hash_password(password: str, salt: str):
    return hashlib.sha256(f'{password}{salt}'.encode()).hexdigest() + f':{salt}'
