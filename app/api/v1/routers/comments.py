from fastapi import Response, status, HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user
from app.models import Comment
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Post
from app import schemas
from typing import List


router = APIRouter(prefix="/api/v1/posts", tags=["Comments"])


@router.get("/{post_id}/comments", response_model=List[schemas.CommentResponse])
def get_post_comments(post_id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user),
                 page_num: int = 1, page_size: int = 10):
    start = (page_num - 1) * page_size
    end = start + page_size

    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at.desc()).slice(start, end).all()
    if not comments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no comments found")
    return comments

@router.post("/{post_id}/comments", status_code=status.HTTP_201_CREATED, response_model=schemas.CommentResponse)
def create_comment(post_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db),
                    current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")

    new_comment = Comment(user_id=current_user.id, post_id=post_id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    if not new_comment:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to create comment")
    return new_comment

@router.put("/{post_id}/comments/{comment_id}", response_model=schemas.CommentResponse)
def comment_update(post_id: int, comment_id: int, updated_comment: schemas.CommentCreate, db: Session = Depends(get_db),
                   current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this comment")

    comment.content = updated_comment.content
    db.commit()
    db.refresh(comment)
    return comment

@router.delete("/{post_id}/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(post_id: int, comment_id: int, db: Session = Depends(get_db),
                    current_user: int = Depends(get_current_user)):
    post = db.query(Post).filter(Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="comment not found")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this comment")

    db.delete(comment)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
