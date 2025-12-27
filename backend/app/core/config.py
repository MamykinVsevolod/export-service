"""
Конфигурация приложения ExportService
Загружает настройки из переменных окружения
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    APP_NAME: str = "ExportService"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Настройки сервера
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Настройки базы данных
    DB_HOST: str = "postgres"
    DB_PORT: int = 5432
    DB_USER: str = "export_user"
    DB_PASSWORD: str = "export_password"
    DB_NAME: str = "export_db"
    
    # Настройки экспорта
    MAX_EXPORT_SIZE: int = 10000
    EXPORT_TIMEOUT: int = 300
    
    @property
    def database_url(self) -> str:
        """Формирует URL для подключения к базе данных"""
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создаем глобальный экземпляр настроек
settings = Settings()