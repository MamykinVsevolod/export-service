"""
Pydantic схемы для валидации данных
Используются для сериализации/десериализации данных в API
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ParsedDataBase(BaseModel):
    """Базовая схема для данных товара"""
    product_name: Optional[str] = None
    price: Optional[Decimal] = None
    old_price: Optional[Decimal] = None
    currency: str = "RUB"
    description: Optional[str] = None
    category: Optional[str] = None
    in_stock: bool = True
    url: Optional[str] = None
    image_url: Optional[str] = None
    brand: Optional[str] = None


class ParsedDataResponse(ParsedDataBase):
    """Схема ответа с данными товара"""
    id: int
    session_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ParsingSessionBase(BaseModel):
    """Базовая схема для парсинг-сессии"""
    session_name: str
    status: str = "completed"
    total_items: int = 0


class ParsingSessionResponse(ParsingSessionBase):
    """Схема ответа с информацией о сессии"""
    id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ParsingSessionWithData(ParsingSessionResponse):
    """Схема сессии с данными товаров"""
    parsed_data: List[ParsedDataResponse] = []
    
    class Config:
        from_attributes = True


class ExportRequest(BaseModel):
    """Схема запроса на экспорт данных"""
    session_id: int = Field(..., description="ID парсинг-сессии для экспорта")
    format: str = Field(..., description="Формат экспорта: csv, json, excel")
    
    class Config:
        json_schema_extra = {
            "example": {
                "session_id": 1,
                "format": "csv"
            }
        }


class ExportHistoryResponse(BaseModel):
    """Схема ответа с историей экспорта"""
    id: int
    session_id: int
    export_format: str
    file_name: str
    file_size: Optional[int] = None
    records_count: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True


class HealthCheckResponse(BaseModel):
    """Схема ответа для проверки здоровья сервиса"""
    status: str
    service: str
    version: str
    database: str