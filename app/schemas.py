"""
Модуль для описания Pydantic-схем.
"""

from typing import List
from pydantic import BaseModel

class PostBase(BaseModel):
    """Базовая схема поста."""
    title: str
    content: str
    user_id: int

class PostCreate(PostBase):
    """Схема для создания поста."""

class Post(PostBase):
    """Схема для отображения поста."""
    id: int

    class Config:
        """Дополнительные настройки."""
        from_attributes = True

class UserBase(BaseModel):
    """Базовая схема пользователя."""
    username: str
    email: str

class UserCreate(UserBase):
    """Схема для создания пользователя."""
    password: str

class User(UserBase):
    """Схема для отображения пользователя."""
    id: int
    posts: List[Post] = []

    class Config:
        """Дополнительные настройки."""
        from_attributes = True
