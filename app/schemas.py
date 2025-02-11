from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr

# -----------------------
# Схемы для пользователей
# -----------------------

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: Optional[str] = "reader"  # По умолчанию роль — "reader"

class UserCreate(UserBase):
    password: str  # Перед созданием пользователя нужно указать пароль

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True  # Позволяет работать с объектами SQLAlchemy

# -----------------------
# Схемы для авторов
# -----------------------

class AuthorBase(BaseModel):
    name: str
    biography: Optional[str] = None
    date_of_birth: Optional[date] = None

class AuthorCreate(AuthorBase):
    pass  # Дополнительные поля можно добавить при необходимости

class AuthorRead(AuthorBase):
    id: int

    class Config:
        orm_mode = True

# -----------------------
# Схемы для жанров
# -----------------------

class GenreBase(BaseModel):
    name: str

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int

    class Config:
        orm_mode = True

# -----------------------
# Схемы для книг
# -----------------------

class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    publication_date: Optional[date] = None
    available_copies: Optional[int] = 1

class BookCreate(BookBase):
    # Для создания книги можно передавать идентификаторы авторов и жанров
    author_ids: List[int] = []
    genre_ids: List[int] = []

class BookRead(BookBase):
    id: int
    # В ответе можно вернуть подробную информацию об авторах и жанрах
    authors: List[AuthorRead] = []
    genres: List[GenreRead] = []

    class Config:
        orm_mode = True

# -----------------------
# Схемы для выдачи книги
# -----------------------

class IssueBase(BaseModel):
    expected_return_date: datetime

class IssueCreate(IssueBase):
    book_id: int
    user_id: int

class IssueRead(IssueBase):
    id: int
    issued_date: datetime
    returned_date: Optional[datetime] = None
    book: BookRead  # Можно добавить подробную информацию о книге
    # При необходимости можно добавить и информацию о пользователе

    class Config:
        orm_mode = True
