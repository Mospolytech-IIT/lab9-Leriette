"""Модуль для обновления данных пользователей и постов в базе данных"""
from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

Session = sessionmaker(bind=engine)
session = Session()

def update_user_email(user_id, new_email):
    """Обновляет email пользователя по его ID"""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
        print(f"Email пользователя с ID {user_id} обновлен на {new_email}.")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

def update_post_content(post_id, new_content):
    """Обновляет содержание поста по его ID"""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
        print(f"Контент поста с ID {post_id} обновлен.")
    else:
        print(f"Пост с ID {post_id} не найден.")

if __name__ == '__main__':
    update_user_email(1, "vika_new@mail.ru")
    update_post_content(1, "Обновленное содержание первого поста.")
