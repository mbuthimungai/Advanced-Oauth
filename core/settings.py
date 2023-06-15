from pydantic import BaseSettings
import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()
class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 4
    ALGORITHM: str = os.getenv("ALGORITHM")
    SQLALCHEMY_DATABASE_URI: str = os.getenv("SQLALCHEMY_DATABASE_URI")
    class Config:
        case_sensitive = True
        
    
@lru_cache()
def get_settings():
    return Settings()
