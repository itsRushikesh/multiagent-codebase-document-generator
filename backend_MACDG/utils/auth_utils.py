from passlib.hash import bcrypt

def hash_password(password: str) -> str:
    pw_bytes = password.encode('utf-8')
    if len(pw_bytes) > 72:
        raise ValueError("Password too long (max 72 UTF-8 bytes). Please use a shorter password.")
    return bcrypt.hash(password)

def verify_password(plain_password: str, password_hash: str) -> bool:
    if len(plain_password.encode('utf-8')) > 72:
        return False
    return bcrypt.verify(plain_password, password_hash)
