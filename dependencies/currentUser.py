from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from dependencies.dbDependency import get_db
from sqlalchemy.orm import Session
from typing import Annotated
from auth.authentication.login import oauth2_scheme
from core.settings import Settings, get_settings
from schemas.TokenSchema.token_schema import TokenData
from cruds.user_cruds import get_user_by_email

def get_current_user(token: Annotated[OAuth2PasswordBearer, Depends(oauth2_scheme)],
                     db: Annotated[Session, Depends(get_db)],
                     settings: Annotated[Settings, Depends(get_settings)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, [settings.ALGORITHM], )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_email(db, token_data.username)
    if user is None:
        raise credentials_exception
    return user