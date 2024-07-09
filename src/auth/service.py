# src/auth/service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException  # Import HTTPException
from .models import User
from .schemas import UserCreate
from .utils import get_password_hash



def authenticate_user(username: str, password: str, db: Session) -> Optional[User]:
    """
    Authenticates a user by checking if the provided username and password match
    the stored credentials in the database.

    Args:
    - username (str): The username of the user to authenticate.
    - password (str): The password of the user to authenticate.
    - db (Session): The database session.

    Returns:
    - Optional[User]: The authenticated user, or None if the authentication fails.
    """
    user = db.query(User).filter(User.username == username).first()
    
    if user and verify_password(password, user.hashed_password):
        return user
    
    return None

def create_user(user_data: UserCreate, db: Session):
    """
    Creates a new user in the database.

    Args:
    - user_data (UserCreate): The user data to be created.
    - db (Session): The database session.

    Returns:
    - User: The created user object.
    """
    # Check if the username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password
    hashed_password = get_password_hash(user_data.password)

    # Create the user object and add it to the database
    user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def create_access_token(data: dict) -> str:
    """
    Create a new access token with the given data.

    Args:
    - data (dict): The data to be encoded in the token.

    Returns:
    - str: The encoded access token.
    """
    expiration_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {**data, "exp": expiration_time}
    encoded_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_token
