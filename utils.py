from passlib.hash import argon2



def get_hash_password(raw_password: str) -> str:
    return argon2.hash(raw_password)


def verify_hash_password(raw_password: str, hash_password: str) -> bool:
    return argon2.verify(raw_password, hash_password)


