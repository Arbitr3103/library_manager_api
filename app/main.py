from fastapi import FastAPI
from app.routers import users, books, authors, genres, auth, issues

app = FastAPI(
    title="Library Manager API",
    description="API для управления библиотекой (книги, авторы, читатели, выдача книг)",
    version="0.1.0"
)

# Подключаем роутеры с префиксами и тегами
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(books.router, prefix="/books", tags=["books"])
app.include_router(authors.router, prefix="/authors", tags=["authors"])
app.include_router(genres.router, prefix="/genres", tags=["genres"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(issues.router, prefix="/issues", tags=["issues"])

@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Library Manager API!"}
