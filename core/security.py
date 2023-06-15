from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import timedelta, datetime
from core.settings import get_settings, Settings
from fastapi import Depends
from typing import Annotated

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(settings: Annotated[Settings, Depends(get_settings)],
                        data: dict,
                        expires_delta: timedelta | None = None
                        ):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)
    return encoded_jwt