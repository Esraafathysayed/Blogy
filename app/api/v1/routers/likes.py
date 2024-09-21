from fastapi import status, HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Likes
from app.models import Post
from app import schemas


router = APIRouter(prefix="/api/v1/likes", tags=["Likes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(like: schemas.LikeRequest, db: Session = Depends(get_db),
         current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == like.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="the post is not found")

    like_query = db.query(Likes).filter(
        Likes.post_id == like.post_id,
        Likes.user_id == current_user.id)
    found_like = like_query.first()

    if like.direction == 1:
        if found_like:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="user has already liked this post")
        new_like = Likes(post_id=like.post_id, user_id=current_user.id)
        db.add(new_like)
        db.commit()
        return {"message": "Successfully liked this post"}
    else:
        if not found_like:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="like already does not exist")
        like_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Successfully deleted like"}
