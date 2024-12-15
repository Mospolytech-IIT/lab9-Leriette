from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

# Удаление одного поста
def delete_post(post_id):
    post = session.query(Post).filter(Post.id == post_id).first()
    if post:
        session.delete(post)
        session.commit()
        print(f"Пост с ID {post_id} удален.")
    else:
        print(f"Пост с ID {post_id} не найден.")

# Удаление пользователя и всех его постов
def delete_user_and_posts(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        # Удаление всех постов пользователя
        session.query(Post).filter(Post.user_id == user_id).delete()
        # Удаление пользователя
        session.delete(user)
        session.commit()
        print(f"Пользователь с ID {user_id} и все его посты удалены.")
    else:
        print(f"Пользователь с ID {user_id} не найден.")

# Пример вызова функций
if __name__ == '__main__':
    delete_post(2)
    delete_user_and_posts(3)
