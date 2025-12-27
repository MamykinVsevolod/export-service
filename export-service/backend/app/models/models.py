"""
Модели данных для работы с базой данных
Описывают структуру таблиц PostgreSQL
"""

from sqlalchemy import Column, Integer, String, DECIMAL, Boolean, Text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.connection import Base


class ParsingSession(Base):
    """Модель для хранения информации о парсинг-сессиях"""
    
    __tablename__ = "parsing_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_name = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False, default="completed")
    created_at = Column(TIMESTAMP, server_default=func.now())
    completed_at = Column(TIMESTAMP, nullable=True)
    total_items = Column(Integer, default=0)
    
    # Связь с данными парсинга
    parsed_data = relationship("ParsedData", back_populates="session", cascade="all, delete-orphan")
    export_history = relationship("ExportHistory", back_populates="session", cascade="all, delete-orphan")


class ParsedData(Base):
    """Модель для хранения спарсенных данных о товарах"""
    
    __tablename__ = "parsed_data"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("parsing_sessions.id", ondelete="CASCADE"), nullable=False)
    product_name = Column(String(500))
    price = Column(DECIMAL(10, 2))
    old_price = Column(DECIMAL(10, 2), nullable=True)
    currency = Column(String(10), default="RUB")
    description = Column(Text, nullable=True)
    category = Column(String(255), nullable=True)
    in_stock = Column(Boolean, default=True)
    url = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    brand = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Связь с сессией
    session = relationship("ParsingSession", back_populates="parsed_data")


class ExportHistory(Base):
    """Модель для хранения истории экспортов"""
    
    __tablename__ = "export_history"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("parsing_sessions.id", ondelete="CASCADE"), nullable=False)
    export_format = Column(String(20), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=True)
    records_count = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    # Связь с сессией
    session = relationship("ParsingSession", back_populates="export_history")