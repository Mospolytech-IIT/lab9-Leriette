"""
Модуль для операций с пользователями в базе данных.
"""
from sqlalchemy.orm import Session
from .. import models, schemas

def get_users(db: Session):
    """Получить всех пользователей из базы данных."""
    return db.query(models.User).all()

def create_user(db: Session, user: schemas.UserCreate):
    """Создать нового пользователя."""
    db_user = models.User(username=user.username, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_email(db: Session, user_id: int, new_email: str):
    """Обновить email пользователя."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.email = new_email
        db.commit()
        return user
    return None

def delete_user(db: Session, user_id: int):
    """Удалить пользователя по ID."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
