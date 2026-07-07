import bcrypt
from fastapi import HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.config import settings

# Password hashing and verification functions
def hash_password(password:str)->str:
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    hash = bcrypt.hashpw(password_bytes, salt)
    return hash.decode('utf-8')

def verify_password(plain_password:str, hashed_password:str)->bool:
    password_bytes = plain_password[:72].encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')

    return bcrypt.checkpw(password_bytes, hashed_bytes)

# jwt token generation and verification functions

def create_access_token(data:dict)->str:
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode,settings.SECRET_KEY, algorithm = settings.ALGORITHM) # This is the function that generates a JWT (JSON Web Token) using the provided data, secret key, and algorithm. It first creates a copy of the input data, adds an expiration time to it, and then encodes it into a JWT string using the specified secret key and algorithm. The resulting token can be used for authentication and authorization purposes in web applications.
    return encoded_jwt

def verify_access_token(token:str)->dict: 

    try:
        payload = jwt.decode(token, settings.SECRET_KEY , algorithms=[settings.ALGORITHM]) # it does 3 things: 1.it verifies the signature of the token using the secret key and algorithm specified. 2. it checks if the token has expired based on the "exp" claim in the payload. 3. it decodes the payload and returns it as a dictionary.

        user_id = payload.get("user_id") # we are extracting the user_id from the payload of the token. This is important because we need to know which user the token belongs to in order to authorize access to protected resources.

        if user_id is None:
            raise None
        
        return payload 
    except JWTError:
        return None




