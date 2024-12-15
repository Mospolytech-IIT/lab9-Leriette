from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Инициализация базы данных
DATABASE_URL = "mysql://lerika:0000@localhost/my_database"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Модель Users
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    posts = relationship('Post', back_populates='user')

# Модель Posts
class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    user = relationship('User', back_populates='posts')

# Создание таблиц
if __name__ == '__main__':
    Base.metadata.create_all(engine)
    print("Таблицы созданы!")
