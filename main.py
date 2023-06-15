from fastapi import FastAPI
from auth.authentication import login, register
from endpoints.users import users
from dotenv import load_dotenv
from database.database import Base, engine

Base.metadata.create_all(engine)
load_dotenv()

app = FastAPI()

app.include_router(login.router)
app.include_router(register.router)
app.include_router(users.router)

