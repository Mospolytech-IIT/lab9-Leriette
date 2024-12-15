"""
Модуль для удаления данных из базы данных.
"""
from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

Session = sessionmaker(bind=engine)
session = Session()

def delete_post(post_id):
    """Удаляет пост по указанному ID."""
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        print(f"Пост с ID {post_id} удален.")
    else:
        print(f"Пост с ID {post_id} не найден.")

def delete_user_and_posts(user_id):
    """Удаляет пользователя и все его посты по указанному ID."""
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        session.query(Post).filter(Post.user_id == user_id).delete()
        session.delete(user)
        session.commit()
        print(f"Пользователь с ID {user_id} и все его посты удалены.")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

if __name__ == '__main__':
    delete_post(2)
    delete_user_and_posts(3)
