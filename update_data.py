from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Обновление email пользователя
def update_user_email(user_id, new_email):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        user.email = new_email
        session.commit()
        print(f"Email пользователя с ID {user_id} обновлен на {new_email}.")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

# Обновление content поста
def update_post_content(post_id, new_content):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        post.content = new_content
        session.commit()
        print(f"Контент поста с ID {post_id} обновлен.")
    else:
        print(f"Пост с ID {post_id} не найден.")

# Пример вызова функций
if __name__ == '__main__':
    update_user_email(1, "vika_new@mail.ru")
    update_post_content(1, "Обновленное содержание первого поста.")
