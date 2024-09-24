from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from .models import User
from .config import settings
from . import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    """Function to create access token
    Args:
        data (dict): User data
    Returns:
        str: Access token
    """
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    """Function to create access token
    Args:
        data (dict): User data
    Returns:
        str: Access token
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_id = payload.get("user_id")
        username = payload.get("username")
        if user_id is None or username is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_id=user_id, username=username)
    except JWTError:
        raise credentials_exception
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Function to get current user
    Args:
        token (str, optional): Access token. Defaults to Depends(oauth2_scheme).
        db (Session, optional): Database session. Defaults to Depends(get_db).
    Returns:
        User: User object
    """
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(User).filter(User.id == token_data.user_id,
                                 User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user
