import hashlib


def hash_string(string: str) -> str:
    return hashlib.sha256(string.encode("utf-8")).hexdigest()


def check_equivalence(string: str, hashed_string: str) -> bool:
    return hash_string(string) == hashed_string
