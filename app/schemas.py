from pydantic import BaseModel, EmailStr, Field, HttpUrl
from datetime import datetime
from typing import Optional, List
from typing_extensions import Annotated


#=============== routers.auth ================#

class UserCreateRequest(BaseModel):
    """
    role: request model for creating a new user
    endpoint: /api/v1/auth/register
    endpoint path: app.api.v1.routers.auth.register
    """
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    phone: str

class UserCreateResponse(BaseModel):
    """
    role: response model for creating a new user
    endpoint: /api/v1/auth/register
    endpoint path: app.api.v1.routers.auth.register
    """
    id: int
    first_name: str
    last_name: str
    phone: int
    username: str
    email: EmailStr
    created_at: datetime
    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    """
    role: response model for user login
    endpoint: /api/v1/auth/login
    endpoint path: app.api.v1.routers.auth.login
    """
    access_token: str
    token_type: str

#=============== routers.post ================#

class AuthorCommResponse(BaseModel):
    """
    helper class for CommentDet
    """
    id: int
    username: str
    class Config:
        from_attributes = True

class AuthorResponse(AuthorCommResponse):
    """
    helper class for PostDet
    """
    email: EmailStr
    class Config:
        from_attributes = True

class CommentDet(BaseModel):
    """
    helper class for PostDet
    """
    id: int
    content: str
    user: AuthorCommResponse
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class PostDet(BaseModel):
    """
    helper class for PostWDetailsResponse
    """
    id: int
    title: str
    content: str
    published: bool = True
    image: Optional[HttpUrl] = None
    user: AuthorResponse
    created_at: datetime
    updated_at: datetime
    comments: List[CommentDet]
    class Config:
        from_attributes = True

class PostWDetailsResponse(BaseModel):
    """
    role: response model for getting all posts and one post
    endpoint: /api/v1/posts/ and /api/v1/posts/{id}
    endpoint path: app.api.v1.routers.post.get_posts/get_post
    """
    Post: PostDet
    likes: Optional[int] = 0
    class Config:
        from_attributes = True

class PostCreateUpdateResponse(BaseModel):
    """
    role: response model for creating and updating a post
    endpoint: /api/v1/posts/ and /api/v1/posts/{id}
    endpoint path: app.api.v1.routers.post.create_post
    """
    id: int
    title: str
    content: str
    image: Optional[HttpUrl] = None
    published: bool = True
    created_at: datetime
    user_id: int
    class Config:
        from_attributes = True

class PostCreateUpdateRequest(BaseModel):
    """
    role: request model for creating and updating a post
    endpoint: /api/v1/posts/ and /api/v1/posts/{id}
    endpoint path: app.api.v1.routers.post.create_post
    """
    title: str
    content: str
    image: Optional[HttpUrl] = None
    published: bool = True
    class Config:
        from_attributes = True

#=============== routers.likes ================#

class LikeRequest(BaseModel):
    """
    role: request model for like and unlike a post
    endpoint: /api/v1/likes/
    endpoint path: app.api.v1.routers.likes.like_post
    """
    post_id: int
    direction: Annotated[int, Field(ge=-1, le=1)]
    class Config:
        from_attributes = True

#=============== routers.user ================#

class UserResponse(BaseModel):
    """
    role: response model for getting a user/users
    endpoint: /api/v1/users/ and /api/v1/users/{id}
    endpoint path: app.api.v1.routers.user.get_user
    """
    id: int
    first_name: str
    last_name: str
    username: str
    bio: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    created_at: datetime
    class Config:
        from_attributes = True

class OneUserResponse(UserResponse):
    """
    role: response model for getting one user
    endpoint: /api/v1/users/{id}
    endpoint path: app.api.v1.routers.user.get_user
    """
    phone: str
    email: EmailStr
    class Config:
        from_attributes = True

class UserUpdateResponse(OneUserResponse):
    """
    role: response model for updating a user
    endpoint: /api/v1/users/{id}
    endpoint path: app.api.v1.routers.user.update_user
    """
    updated_at: datetime

class UserUpdateRequest(BaseModel):
    """
    role: request model for updating a user
    endpoint: /api/v1/users/{id}
    endpoint path: app.api.v1.routers.user.update_user
    """
    first_name: str
    last_name: str
    phone: str
    username: str
    email: EmailStr
    bio: Optional[str] = None
    avatar: Optional[HttpUrl] = None
    class Config:
        from_attributes = True

#=============== routers.comments ================#

# class CommentResponse(BaseModel):
#     user_id: int
#     post_id: int
#     content: str
#     created_at: datetime
#     updated_at: datetime
#     class Config:
#         from_attributes = True

class CommentResponse(BaseModel):
    id: int
    post_id: int
    content: str
    user: AuthorCommResponse
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str
    class Config:
        from_attributes = True




























class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenData(BaseModel):
    user_id: int
    username: str
