import os
from dotenv import load_dotenv  # Импортируем функцию для загрузки .env
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем URL подключения из переменной окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Создаем движок SQLAlchemy. echo=True можно отключить для продакшена.
engine = create_engine(DATABASE_URL, echo=True)

# Фабрика сессий для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

