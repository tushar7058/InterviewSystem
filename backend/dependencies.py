from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.models import SessionLocal
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from backend.config import settings

# Dependency for database session

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependency for OAuth2 authentication

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
