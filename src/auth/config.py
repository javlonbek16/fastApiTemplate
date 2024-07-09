SECRET_KEY = "very_very_secret_word"  # Replace with a strong, random secret key
ALGORITHM = "HS256"  # Replace with the desired algorithm for JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Replace with the desired expiration time in minutes

# src/config.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:postgres@192.168.13.85/forTemplate"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
