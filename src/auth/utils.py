import bcrypt

def verify_password(plain_password, hashed_password):
    """
    Verify if the plain password matches the hashed password.
    
    Args:
    - plain_password (str): The plain text password to verify.
    - hashed_password (str): The hashed password stored in the database.
    
    Returns:
    - bool: True if the plain password matches the hashed password, False otherwise.
    """
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    """
    Generate a bcrypt hash of the given password.

    Args:
    - password (str): The plain text password to hash.

    Returns:
    - str: The hashed password as a string.
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_bytes.decode('utf-8')