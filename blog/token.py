from datetime import datetime, timedelta
from typing import Union
from jose import jwt, JWTError

from .sechams import TokenData

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "184ece819a5e609be002439291015969070ae30a78c2b6d85d54f8ed059f42fc"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30



def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(data:str, credentials_exception):
    try:
        payload = jwt.decode(data, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        data = TokenData(username=email)
    except JWTError:
        raise credentials_exception

    return data
   