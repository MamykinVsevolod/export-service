"""
Модуль для работы с базой данных
Настройка подключения к PostgreSQL через SQLAlchemy
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создаем движок базы данных
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,  # проверка соединения перед использованием
    echo=settings.DEBUG   # логирование SQL-запросов в режиме отладки
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()


def get_db():
    """
    Генератор для получения сессии базы данных
    Используется как зависимость в FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()