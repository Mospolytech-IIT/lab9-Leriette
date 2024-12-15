from pydantic import BaseModel
from typing import List, Optional

class PostBase(BaseModel):
    title: str
    content: str
    user_id: int

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    posts: List[Post] = []
    class Config:
        from_attributes = True

