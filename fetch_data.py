"""
Модуль для извлечения и отображения данных из базы данных.
"""
from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

Session = sessionmaker(bind=engine)
session = Session()

users = session.query(User).all()
print("Все пользователи:")
for user in users:
    print(f"User ID: {user.id}, Username: {user.username}, "
          f"Email: {user.email}, Password: {user.password}")
print()

posts = session.query(Post).all()
print("Все посты с информацией о пользователях:")
for post in posts:
    print(f"Post ID: {post.id}, Title: {post.title}, Content: {post.content}, "
          f"User: {post.user.username} (Email: {post.user.email})")
print()

user_posts = session.query(Post).filter(Post.user_id == 2).all()
print("Посты пользователя с ID 2:")
for post in user_posts:
    print(f"Содержимое: {post.content}")

session.close()
