# src/auth/router.py

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .schemas import Token, UserCreate, User
from .service import authenticate_user, create_access_token, create_user as db_create_user
from .dependencies import get_db, get_current_user
from .models import User as DBUser 

router = APIRouter()



@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> dict:
    """
    Endpoint to authenticate a user and generate an access token.

    Args:
        form_data (OAuth2PasswordRequestForm): The form data containing the username and password.
        db (Session): The database session.

    Returns:
        dict: A dictionary containing the access token and token type.

    Raises:
        HTTPException: If the username or password is incorrect.
    """
    # Authenticate the user
    user = authenticate_user(form_data.username, form_data.password, db)
    
    # If the user is not authenticated, raise an exception
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    # Generate an access token with the user's username as the subject
    access_token = create_access_token(
        data={"sub": user.username}
    )
    
    # Return the access token and token type as a dictionary
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.post("/users/", response_model=User)
def create_user(
    user_create: UserCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new user.

    Parameters:
    - user_create (UserCreate): The user data to be created.
    - db (Session): The database session.

    Returns:
    - User: The created user object.
    """
    return db_create_user(user_create, db=db)

@router.get("/users/me", response_model=User)
def read_user_details(user: User = Depends(get_current_user)):
    """
    Get the details of the currently authenticated user.

    Parameters:
    - user (User): The currently authenticated user.

    Returns:
    - User: The user details.
    """
    return user
