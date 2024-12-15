"""
Модуль для добавления тестовых данных в базу данных.
"""
from sqlalchemy.orm import sessionmaker
from models import engine, User, Post

Session = sessionmaker(bind=engine)
session = Session()

user1 = User(username='Vika', email='vika@mail.ru', password='12345')
user2 = User(username='Lana', email='lana@mail.ru', password='password')
user3 = User(username='Masha', email='masha@mail.ru', password='white')
session.add_all([user1, user2, user3])
session.commit()

post1 = Post(title='Первый пост', content='Это содержание первого поста', user_id=user1.id)
post2 = Post(title='Второй пост', content='Это содержание второго поста', user_id=user2.id)
post3 = Post(title='Третий пост', content='Это содержание третьего поста', user_id=user3.id)
session.add_all([post1, post2, post3])
session.commit()

print("Данные добавлены!")
