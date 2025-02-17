from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import hash_password  # Функция хэширования пароля
from datetime import datetime, timezone

# -----------------------------
# CRUD операции для пользователей
# -----------------------------
def create_user(db: Session, user: schemas.UserCreate):
    # Хэшируем пароль перед сохранением
    hashed_pwd = hash_password(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# Новая функция: получить пользователя по username
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

# Функция обновления пользователя
def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user

# Функция удаления пользователя
def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id)
    if not db_user:
        return None
    db.delete(db_user)
    db.commit()
    return db_user


# -----------------------------
# CRUD операции для авторов
# -----------------------------
def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(
        name=author.name,
        biography=author.biography,
        date_of_birth=author.date_of_birth
    )
    db.add(db_author)
    db.commit()
    db.refresh(db_author)
    return db_author


def get_author(db: Session, author_id: int):
    return db.query(models.Author).filter(models.Author.id == author_id).first()


def get_authors(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Author).offset(skip).limit(limit).all()


# -----------------------------
# CRUD операции для книг
# -----------------------------
def create_book(db: Session, book: schemas.BookCreate):
    # Попытаемся найти книгу с таким же названием
    existing_book = db.query(models.Book).filter(models.Book.title == book.title).first()
    if existing_book:
        # Обновляем количество доступных экземпляров
        existing_book.available_copies += book.available_copies
        db.commit()
        db.refresh(existing_book)
        return existing_book
    else:
        db_book = models.Book(
            title=book.title,
            description=book.description,
            publication_date=book.publication_date,
            available_copies=book.available_copies,
        )
        db.add(db_book)
        db.commit()
        db.refresh(db_book)
        # Добавляем авторов и жанры
        for author_id in book.author_ids:
            db_author = db.query(models.Author).get(author_id)
            if db_author:
                db_book.authors.append(db_author)
        for genre_id in book.genre_ids:
            db_genre = db.query(models.Genre).get(genre_id)
            if db_genre:
                db_book.genres.append(db_genre)
        db.commit()
        db.refresh(db_book)
        return db_book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()


def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

def return_book(db: Session, issue_id: int):
    # Находим запись выдачи книги по её ID
    db_issue = db.query(models.Issue).filter(models.Issue.id == issue_id).first()
    if not db_issue or db_issue.returned_date is not None:
        # Либо выдача не найдена, либо книга уже возвращена
        return None
    # Фиксируем дату возврата с привязанной временной зоной
    db_issue.returned_date = datetime.now(timezone.utc)
    # Увеличиваем количество доступных экземпляров книги
    book = db.query(models.Book).filter(models.Book.id == db_issue.book_id).first()
    if book:
        book.available_copies += 1
    db.commit()
    db.refresh(db_issue)
    return db_issue


def delete_book(db: Session, book_id: int):
    db_book = get_book(db, book_id)
    if db_book is None:
        return None
    db.delete(db_book)
    db.commit()
    return db_book


# -----------------------------
# CRUD операции для жанров
# -----------------------------
def create_genre(db: Session, genre: schemas.GenreCreate):
    db_genre = models.Genre(name=genre.name)
    db.add(db_genre)
    db.commit()
    db.refresh(db_genre)
    return db_genre


def get_genre(db: Session, genre_id: int):
    return db.query(models.Genre).filter(models.Genre.id == genre_id).first()


def get_genres(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Genre).offset(skip).limit(limit).all()


# -----------------------------
# CRUD операции для выдачи книги (Issues)
# -----------------------------
def create_issue(db: Session, issue: schemas.IssueCreate):
    # Проверяем, сколько книг уже выданы данному пользователю (не возвращено)
    current_issues_count = (
        db.query(models.Issue)
        .filter(models.Issue.user_id == issue.user_id, models.Issue.returned_date.is_(None))
        .count()
    )
    if current_issues_count >= 5:
        raise Exception("User already has 5 issued books.")

    # Проверяем, существует ли книга и доступны ли экземпляры
    book = db.query(models.Book).filter(models.Book.id == issue.book_id).first()
    if not book:
        raise Exception("Book not found.")
    if book.available_copies < 1:
        raise Exception("No available copies for this book.")

    # Уменьшаем количество доступных экземпляров книги
    book.available_copies -= 1

    # Создаем запись о выдаче книги
    db_issue = models.Issue(
        book_id=issue.book_id,
        user_id=issue.user_id,
        expected_return_date=issue.expected_return_date
    )
    db.add(db_issue)
    db.commit()
    db.refresh(db_issue)
    return db_issue


def get_issue(db: Session, issue_id: int):
    return db.query(models.Issue).filter(models.Issue.id == issue_id).first()


def get_issues(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Issue).offset(skip).limit(limit).all()

