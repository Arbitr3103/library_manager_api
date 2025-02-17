from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

# -----------------------
# Схемы для пользователей
# -----------------------

class UserBase(BaseModel):
    username: str = Field(..., example="john_doe")
    email: EmailStr = Field(..., example="john.doe@example.com")
    role: Optional[str] = Field(default="reader", example="reader")  # По умолчанию роль — "reader"

class UserCreate(UserBase):
    password: str = Field(..., example="securepassword123")

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True  # Позволяет работать с объектами SQLAlchemy

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, example="new_username")
    email: Optional[EmailStr] = Field(None, example="new_email@example.com")
    role: Optional[str] = Field(None, example="admin")

    class Config:
        orm_mode = True

# -----------------------
# Схемы для авторов
# -----------------------

class AuthorBase(BaseModel):
    name: str = Field(..., example="J.K. Rowling")
    biography: Optional[str] = Field(default=None, example="British author, best known for the Harry Potter series.")
    date_of_birth: Optional[date] = Field(default=None, example="1965-07-31")

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
    name: str = Field(..., example="Fantasy")

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
    title: str = Field(..., example="Harry Potter and the Sorcerer's Stone")
    description: Optional[str] = Field(default=None, example="A young wizard's journey begins.")
    publication_date: Optional[date] = Field(default=None, example="1997-06-26")
    available_copies: Optional[int] = Field(default=1, example=10)

class BookCreate(BookBase):
    # Для создания книги можно передавать идентификаторы авторов и жанров
    author_ids: List[int] = Field(default_factory=list, example=[1])
    genre_ids: List[int] = Field(default_factory=list, example=[1])

class BookRead(BookBase):
    id: int
    # В ответе можно вернуть подробную информацию об авторах и жанрах
    authors: List[AuthorRead] = Field(default_factory=list)
    genres: List[GenreRead] = Field(default_factory=list)

    class Config:
        orm_mode = True

# -----------------------
# Схемы для выдачи книги
# -----------------------

class IssueBase(BaseModel):
    expected_return_date: datetime = Field(..., example="2025-03-01T15:30:00")

class IssueCreate(IssueBase):
    book_id: int = Field(..., example=1)
    user_id: int = Field(..., example=1)

class IssueRead(IssueBase):
    id: int
    issued_date: datetime = Field(..., example="2025-02-13T12:45:38")
    returned_date: Optional[datetime] = Field(default=None, example="2025-02-20T12:45:38")
    book: BookRead  # Можно добавить подробную информацию о книге
    # При необходимости можно добавить и информацию о пользователе

    class Config:
        orm_mode = True
