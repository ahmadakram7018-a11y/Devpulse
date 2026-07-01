import bcrypt
def hash_password(password:str)->str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(password_bytes, salt)
    return hash.decode('utf-8')

def verify_password(plain_password:str, hashed_password:str)->bool:
    plain_password = bcrypt.hashpw(plain_password.encode('utf-8'))
    hashed_password = bcrypt.hashpw(hashed_password.encode('utf-8'))

    return bcrypt.checkpw(plain_password, hashed_password)










