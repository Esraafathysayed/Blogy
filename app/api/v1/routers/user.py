from fastapi import status, HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app import schemas
from typing import List


router = APIRouter(prefix="/api/v1/users", tags=["Users"])


@router.get('/', response_model=List[schemas.UserResponse])
def get_users(page_num: int =  1, page_size: int = 10, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
	start = (page_num - 1) * page_size
	end = start + page_size
	users = db.query(User).slice(start, end).all()
	return users

@router.get("/{id}", response_model=schemas.OneUserResponse)
def get_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
	user = db.query(User).filter(User.id == id).first()

	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
	if user.id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this user")
	return user

@router.put("/{id}", response_model=schemas.UserUpdateResponse)
def update_user(id: int, updated_user: schemas.UserUpdateRequest, db: Session = Depends(get_db),
				current_user: int = Depends(get_current_user)):
	user = db.query(User).filter(User.id == id)
	if not user.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
	if user.first().id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this user")
	if user.first().phone != updated_user.phone:
		if db.query(User).filter(User.phone == updated_user.phone).first():
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="phone number already in use")
	if updated_user.username != user.first().username:
		if db.query(User).filter(User.username == updated_user.username).first():
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="username already taken")
	if updated_user.email != updated_user.email:
		if db.query(User).filter(User.email == updated_user.email).first():
			raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="email already taken")

	user.update(updated_user.dict(), synchronize_session=False)
	db.commit()
	db.refresh(user.first())
	return user.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
	user = db.query(User).filter(User.id == id)

	if not user.first():
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
	if user.first().id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this user")

	user.delete(synchronize_session=False)
	db.commit()
	return None