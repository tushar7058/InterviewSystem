from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
import os

router = APIRouter()

# In-memory user store (replace with DB in production)
users = {}

SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict):
    from datetime import datetime, timedelta
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(hours=1)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

@router.post("/register/")
def register(user: User):
    if user.username in users:
        raise HTTPException(status_code=400, detail="Username already registered.")
    users[user.username] = get_password_hash(user.password)
    return {"message": "User registered successfully."}

@router.post("/login/", response_model=Token)
def login(user: User):
    hashed_password = users.get(user.username)
    if not hashed_password or not verify_password(user.password, hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    access_token = create_access_token({"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
