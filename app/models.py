import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Text,
    DateTime,
    ForeignKey,
    Table,
)
from sqlalchemy.orm import declarative_base, relationship

# Создаем базовый класс для моделей
Base = declarative_base()

# Таблица для связи "многие-ко-многим" между книгами и авторами
book_author = Table(
    'book_author',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

# Таблица для связи "многие-ко-многим" между книгами и жанрами
book_genre = Table(
    'book_genre',
    Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True)
)


# Модель пользователя: читатель или администратор
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="reader")  # возможные значения: "reader", "admin"


# Модель автора
class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    biography = Column(Text)
    date_of_birth = Column(Date)

    # Связь с книгами (многие ко многим)
    books = relationship("Book", secondary=book_author, back_populates="authors")


# Модель жанра
class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    # Связь с книгами (многие ко многим)
    books = relationship("Book", secondary=book_genre, back_populates="genres")


# Модель книги
class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text)
    publication_date = Column(Date)
    available_copies = Column(Integer, default=1)

    # Связи: с авторами, жанрами и выдачами
    authors = relationship("Author", secondary=book_author, back_populates="books")
    genres = relationship("Genre", secondary=book_genre, back_populates="books")
    issues = relationship("Issue", back_populates="book")


# Модель выдачи книги
class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, ForeignKey("books.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    issued_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    expected_return_date = Column(DateTime)
    returned_date = Column(DateTime, nullable=True)  # Поле заполнится при возврате книги

    # Связи с книгой и пользователем
    book = relationship("Book", back_populates="issues")
    user = relationship("User")
