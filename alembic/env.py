import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Загружаем переменные окружения из .env
load_dotenv()

# Получаем конфигурацию Alembic
config = context.config

# Устанавливаем URL подключения к базе данных из переменной окружения
config.set_main_option('sqlalchemy.url', os.getenv("DATABASE_URL"))

# Настраиваем логирование (если необходимо)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Импортируем базу моделей
from app.models import Base  # убедись, что путь правильный
target_metadata = Base.metadata

def run_migrations_offline():
    """Запуск миграций в офлайн режиме."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Запуск миграций в онлайн режиме."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

