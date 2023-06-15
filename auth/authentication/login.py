from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from dependencies.dbDependency import get_db
from schemas.userSchema.userschema import UserCreate, User
from schemas.TokenSchema.token_schema import Token
from typing import Annotated
from sqlalchemy.orm import Session
from cruds.user_cruds import get_user_by_email
from core.security import verify_password
from datetime import timedelta
from core.settings import Settings
from dependencies.tokenDependency import create_access_token
router = APIRouter(
    
    tags=["authentication"],
    dependencies=[Depends(get_db)]
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Annotated[Session, router.dependencies[0]],
                                 
                                 ):
    settings = Settings()
    user = get_user_by_email(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"}
        )
    if not verify_password(plain_password=form_data.password,
                           hashed_password=user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    acess_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )  
    return {"access_token": acess_token, "token_type": "bearer"}

