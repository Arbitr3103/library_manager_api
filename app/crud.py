from sqlalchemy.orm import Session
from app import models, schemas

# -----------------------------
# CRUD операции для пользователей
# -----------------------------

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email, hashed_password=user.password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()

# -----------------------------
# CRUD операции для авторов
# -----------------------------

def create_author(db: Session, author: schemas.AuthorCreate):
    db_author = models.Author(name=author.name, biography=author.biography, date_of_birth=author.date_of_birth)
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
        db_book.authors.append(db_author)
    for genre_id in book.genre_ids:
        db_genre = db.query(models.Genre).get(genre_id)
        db_book.genres.append(db_genre)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_book(db: Session, book_id: int):
    return db.query(models.Book).filter(models.Book.id == book_id).first()

def get_books(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Book).offset(skip).limit(limit).all()

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
# CRUD операции для выдачи книги
# -----------------------------

def create_issue(db: Session, issue: schemas.IssueCreate):
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
