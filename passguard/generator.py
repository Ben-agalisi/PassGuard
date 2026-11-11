import secrets
import string


def generate_password(length=16):
    """Generate a random secure password of the given length."""
    characters = string.ascii_letters + string.digits + string.punctuation

    password = [
        secrets.choice(string.ascii_uppercase),
        secrets.choice(string.ascii_lowercase),
        secrets.choice(string.digits),
        secrets.choice(string.punctuation),
    ]
    for i in range(length - 4):
        password.append(secrets.choice(characters))
    secrets.SystemRandom().shuffle(password)
    return ''.join(password)