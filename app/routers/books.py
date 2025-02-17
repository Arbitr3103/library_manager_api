from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db
from app.security import get_current_admin  # Зависимость для проверки прав администратора

router = APIRouter(tags=["books"])

@router.post("/", response_model=schemas.BookRead)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    _current_admin = Depends(get_current_admin)  # Только администратор может создавать книги
):
    return crud.create_book(db=db, book=book)

@router.get("/{book_id}", response_model=schemas.BookRead)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db=db, book_id=book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.get("/", response_model=List[schemas.BookRead])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    books = crud.get_books(db=db, skip=skip, limit=limit)
    return books

@router.delete("/{book_id}", response_model=schemas.BookRead)
def delete_book_endpoint(
    book_id: int,
    db: Session = Depends(get_db),
    _current_admin = Depends(get_current_admin)  # Только администратор может удалять книги
):
    deleted_book = crud.delete_book(db, book_id)
    if deleted_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return deleted_book

