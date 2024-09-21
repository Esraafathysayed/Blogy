from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from app.utils import hash_password, authenticate_user
from app.oauth2 import create_access_token
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import User
from sqlalchemy import or_
from app import schemas


router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post("/login", response_model=schemas.TokenResponse)
def user_login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, user_credentials.username, user_credentials.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(data={"user_id": user.id, "username": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def user_register(user: schemas.UserCreateRequest, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(
        or_(User.username == user.username, User.email == user.email, User.phone == str(user.phone))).first()
    if existing_user:
        if existing_user.username == user.username and existing_user.email == user.email and existing_user.phone == user.phone:
            detail = "Username, email, and phone number already exist"
        elif existing_user.username == user.username and existing_user.email == user.email:
            detail = "Username and email already exist"
        elif existing_user.username == user.username and existing_user.phone == user.phone:
            detail = "Username and phone number already exist"
        elif existing_user.email == user.email and existing_user.phone == user.phone:
            detail = "Email and phone number already exist"
        elif existing_user.username == user.username:
            detail = "Username already exists"
        elif existing_user.email == user.email:
            detail = "Email already exists"
        elif existing_user.phone == user.phone:
            detail = "Phone number already exists"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = User(**user.dict())

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
