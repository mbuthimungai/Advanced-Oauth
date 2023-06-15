from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from core.settings import  Settings



settings = Settings()



engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, 
                            bind=engine)
Base = declarative_base()
