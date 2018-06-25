"""
security/password.py is the file that handles password security/testing.

Hashing algorithm used is SHA256, using a builtin python library hashlib for hashing.
"""

import hashlib


def hash_password(password):
    """
    Hashes the parameter password (String) and returns it in hexadecimal.

    :returns password in hexadecimal
        password: String
    """
    sh = hashlib.sha256()
    sh.update(password)
    return sh.hexdigest()


def compare_passwords(pw1, pw2):
    """
    Compares two (hashed) passwords and returns result.

    :returns if they are identical
        boolean
    """
    if pw1 == pw2:
        return True
    return False
