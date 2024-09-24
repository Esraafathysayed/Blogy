from passlib.context import CryptContext
from sqlalchemy.orm import Session
from .models import User


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    """Hash the password using bcrypt
    Args:
        password (str): The password to hash
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """Verify the password
    Args:
        plain_password (str): The plain password
        hashed_password (str): The hashed password
    Returns:
        bool: True if the password is valid, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    """Authenticate the user
    Args:
        db (Session): Database session
        email (str): The email of the user
        password (str): The password of the user
    Returns:
        User: The user object if the user is authenticated, False otherwise
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.password):
        return False
    return user
