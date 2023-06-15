from fastapi import APIRouter, Depends, HTTPException, status
from dependencies.dbDependency import get_db
from typing import Annotated
from sqlalchemy.orm import Session
from cruds.user_cruds import create_user, get_user_by_email
from schemas.userSchema.userschema import UserCreate, User

router = APIRouter(
    prefix="/api/v1",
    tags=["authentication"],
    dependencies=[Depends(get_db)]
)



@router.post("/register", response_model=User)
def register_user_account(user: UserCreate ,db: Annotated[Session, router.dependencies[0]]):
    print(user)
    user_dict = get_user_by_email(db=db, email=user.email)
    if user_dict:
        raise HTTPException(status_code=409, 
                             detail="user email already exists!")
    user = create_user(db=db, user=user)
    return user


