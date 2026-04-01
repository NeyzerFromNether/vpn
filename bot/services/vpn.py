import random
import string


def generate_key(length: int = 32) -> str:
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def format_key(key: str) -> str:
    chunks = [key[i:i+4] for i in range(0, len(key), 4)]
    return '-'.join(chunks)
