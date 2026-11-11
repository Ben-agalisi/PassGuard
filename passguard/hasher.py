import hashlib

def hash_password(password):
    """Convert a password to its SHA-256 hash."""
    return hashlib.sha256(password.encode()).hexdigest()
