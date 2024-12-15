from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

Session = sessionmaker(bind=engine)
session = Session()

# Извлечение всех пользователей с полной информацией
users = session.query(User).all()
print("Все пользователи:")
for user in users:
    print(f"User ID: {user.id}, Username: {user.username}, Email: {user.email}, Password: {user.password}")
print()

# Извлечение всех постов с полной информацией о пользователях
posts = session.query(Post).all()
print("Все посты с информацией о пользователях:")
for post in posts:
    print(f"Post ID: {post.id}, Title: {post.title}, Content: {post.content}, "
          f"User: {post.user.username} (Email: {post.user.email})")
print()

# Извлечение постов конкретного пользователя (например, user_id = 2)
user_posts = session.query(Post).filter(Post.user_id == 2).all()
print("Посты пользователя с ID 2:")
for post in user_posts:
    print(f"Содержимое: {post.content}")

# Закрываем сессию
session.close()


