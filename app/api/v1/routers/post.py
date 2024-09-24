from fastapi import Response, status, HTTPException, Depends, APIRouter
from app.oauth2 import get_current_user
from app.models import Comment
from app.database import get_db
from sqlalchemy.orm import Session
from app.models import Likes
from app.models import Post
from sqlalchemy import func, select
from app import schemas
from typing import List


router = APIRouter(prefix="/api/v1/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostWDetailsResponse])
def get_posts(page_num: int =  1, page_size: int = 10, db: Session = Depends(get_db)):
    """Get all posts
    Args:
        page_num (int, optional): Page number. Defaults to 1.
        page_size (int, optional): Page size. Defaults to 10.
        db (Session, optional): Database session. Defaults to Depends(get_db).
    Returns:
        List[schemas.PostWDetailsResponse]: List of posts
    """
    start = (page_num - 1) * page_size
    end = start + page_size

    likes_subquery = select(func.count(Likes.id).label("likes"), Likes.post_id)\
        .group_by(Likes.post_id).subquery()
    
    posts = db.query(Post, likes_subquery.c.likes)\
        .outerjoin(likes_subquery, Post.id == likes_subquery.c.post_id)\
        .join(Comment, Comment.post_id == Post.id, isouter=True)\
        .group_by(Post.id, likes_subquery.c.likes)\
        .order_by( Post.created_at.desc()).slice(start, end).all()
    return posts

@router.get("/{id}", response_model=schemas.PostWDetailsResponse)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """Get a post
    Args:
        id (int): Post ID
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (int, optional): Current user. Defaults to Depends(get_current_user).
    Raises:
        HTTPException: [description]
    Returns:
        schemas.PostWDetailsResponse: Post details
    """
    likes_subquery = select(func.count(Likes.id).label("likes"), Likes.post_id)\
        .group_by(Likes.post_id).subquery()

    posts = db.query(Post, likes_subquery.c.likes)\
        .outerjoin(likes_subquery, Post.id == likes_subquery.c.post_id)\
        .join(Comment, Comment.post_id == Post.id, isouter=True)\
        .group_by(Post.id, likes_subquery.c.likes)\
        .order_by( Post.created_at.desc()).filter(Post.id == id).first()

    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    if posts[0].user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this post")
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostCreateUpdateResponse)
def create_post(post: schemas.PostCreateUpdateRequest, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    """Create a post
    Args:
        post (schemas.PostCreateUpdateRequest): Post data
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (int, optional): Current user. Defaults to Depends(get_current_user).
    Returns:
        Post: Post object
    """
    new_post = Post(user_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.put("/{id}", response_model=schemas.PostCreateUpdateResponse)
def update_post(id: int, updated_post: schemas.PostCreateUpdateRequest, db: Session = Depends(get_db),
                current_user: int = Depends(get_current_user)):
    """Update a post
    Args:
        id (int): Post ID
        updated_post (schemas.PostCreateUpdateRequest): Updated post data
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (int, optional): Current user. Defaults to Depends(get_current_user).
    Raises:
        HTTPException: [description]
    Returns:
        Post: Post object
    """
    post = db.query(Post).filter(Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this post")

    post.update(updated_post.dict() ,synchronize_session=False)
    db.commit()
    return post.first()

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int ,db: Session = Depends(get_db), current_user: int = Depends(get_current_user)):
    """Delete a post
    Args:
        id (int): Post ID
        db (Session, optional): Database session. Defaults to Depends(get_db).
        current_user (int, optional): Current user. Defaults to Depends(get_current_user).
    Raises:
        HTTPException: [description]
    Returns:
        Response: Response object
    """
    post = db.query(Post).filter(Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    if post.first().user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you are not the owner of this post")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
