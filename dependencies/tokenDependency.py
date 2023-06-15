from jose import jwt, JWTError
from datetime import timedelta, datetime
from core.settings import Settings
from fastapi import Depends
from typing import Annotated

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    settings = Settings()
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    print(encoded_jwt)
    return encoded_jwt


    
    

