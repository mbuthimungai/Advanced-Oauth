from sqlalchemy.orm import Session
from models.User.userModel import User
from schemas.userSchema.userschema import UserCreate
from core.security import get_password_hash


def get_user(db: Session, user_id: int):
    """Queries for a single user by a user id"""
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    """Queries for a single user by email"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    """Creates a user instance on the database"""
    hashed_password = get_password_hash(password=user.password)
    db_user = User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
