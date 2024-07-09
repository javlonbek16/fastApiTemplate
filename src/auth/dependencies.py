from fastapi import Depends, HTTPException
from jose import jwt, JWTError
from .config import SECRET_KEY, ALGORITHM
from .models import User
from fastapi.security import OAuth2PasswordBearer
from .config import get_session
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception


def get_db() -> Session:
    db = next(get_session())
    try:
        yield db
    finally:
        db.close()