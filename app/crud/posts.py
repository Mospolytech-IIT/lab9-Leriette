"""
Модуль для операций с постами в базе данных.
"""
from sqlalchemy.orm import Session
from .. import models, schemas

def get_posts(db: Session):
    """Получить все посты из базы данных."""
    return db.query(models.Post).all()

def create_post(db: Session, post: schemas.PostCreate):
    """Создать новый пост."""
    db_post = models.Post(title=post.title, content=post.content, user_id=post.user_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post_content(db: Session, post_id: int, new_content: str):
    """Обновить содержимое поста."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        post.content = new_content
        db.commit()
        return post
    return None

def delete_post(db: Session, post_id: int):
    """Удалить пост по ID."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post:
        db.delete(post)
        db.commit()
        return True
    return False
