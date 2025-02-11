from fastapi import FastAPI

# Создаем экземпляр приложения FastAPI
app = FastAPI(
    title="Library Manager API",
    description="API для управления библиотекой (книги, авторы, читатели, выдача книг)",
    version="0.1.0"
)


# Простой эндпоинт для проверки работы приложения
@app.get("/")
def read_root():
    return {"message": "Добро пожаловать в Library Manager API!"}

# Здесь позже можно будет подключать роутеры из app/routers, например:
# from app.routers import books, authors, auth, readers, issues
# app.include_router(books.router)
# app.include_router(auth.router)
# и т.д.
