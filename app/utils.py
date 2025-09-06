# from passlib.context import CryptContext

# pwd_context = CryptContext(schemes="bcrypt", deprecated="auto")

# def hash(password: str):
#     return pwd_context.hash(password)

# def verify(password: str, hashed_password: str):
#     return pwd_context.verify(password, hashed_password)

import bcrypt

def hash(password: str) -> str:
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_password.decode('utf-8')

def verify(password: str, hashed_password: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)