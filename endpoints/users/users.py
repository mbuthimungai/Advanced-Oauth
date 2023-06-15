from fastapi import APIRouter, Depends
from typing import Annotated
from schemas.userSchema import userschema
from dependencies.currentUser import get_current_user
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"],
    dependencies=[]
)

@router.get("/me", response_model=userschema.User)
async def read_users_me(current_user: Annotated[userschema.User, Depends(get_current_user)]):
    return current_user
