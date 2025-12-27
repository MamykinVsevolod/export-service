"""
API маршруты для ExportService
Определяет все endpoints для работы с экспортом данных
"""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from typing import List
from app.database.connection import get_db
from app.schemas.schemas import (
    ParsingSessionResponse,
    ParsingSessionWithData,
    ExportRequest,
    ExportHistoryResponse,
    HealthCheckResponse
)
from app.models.models import ParsingSession, ParsedData, ExportHistory
from app.services.export_service import ExportService
from app.core.config import settings

# Создаем роутер
router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse, tags=["Health"])
async def health_check(db: Session = Depends(get_db)):
    """
    Проверка работоспособности сервиса
    Возвращает статус сервиса и подключения к БД
    """
    try:
        # Проверяем подключение к БД
        from sqlalchemy import text
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy" if db_status == "connected" else "unhealthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "database": db_status
    }


@router.get("/sessions", response_model=List[ParsingSessionResponse], tags=["Sessions"])
async def get_sessions(db: Session = Depends(get_db)):
    """
    Получить список всех парсинг-сессий
    Возвращает информацию о доступных сессиях для экспорта
    """
    sessions = db.query(ParsingSession).all()
    return sessions


@router.get("/sessions/{session_id}", response_model=ParsingSessionWithData, tags=["Sessions"])
async def get_session_with_data(session_id: int, db: Session = Depends(get_db)):
    """
    Получить детальную информацию о сессии с данными
    
    Args:
        session_id: ID парсинг-сессии
    
    Returns:
        Информация о сессии и список всех спарсенных товаров
    """
    session = db.query(ParsingSession).filter(ParsingSession.id == session_id).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    return session


@router.post("/export", tags=["Export"])
async def export_data(
    export_request: ExportRequest,
    db: Session = Depends(get_db)
):
    """
    Экспортировать данные парсинга в указанном формате
    
    Args:
        export_request: Запрос с ID сессии и форматом экспорта
    
    Returns:
        Файл в запрошенном формате (CSV, JSON или Excel)
    """
    # Проверяем существование сессии
    session = db.query(ParsingSession).filter(
        ParsingSession.id == export_request.session_id
    ).first()
    
    if not session:
        raise HTTPException(status_code=404, detail="Сессия не найдена")
    
    # Проверяем наличие данных
    data_count = db.query(ParsedData).filter(
        ParsedData.session_id == export_request.session_id
    ).count()
    
    if data_count == 0:
        raise HTTPException(status_code=404, detail="Нет данных для экспорта")
    
    # Создаем сервис экспорта
    export_service = ExportService(db)
    
    # Экспортируем в зависимости от формата
    format_lower = export_request.format.lower()
    
    if format_lower == "csv":
        file_data = export_service.export_to_csv(export_request.session_id)
        media_type = "text/csv"
        filename = f"export_{export_request.session_id}.csv"
        
    elif format_lower == "json":
        file_data = export_service.export_to_json(export_request.session_id)
        media_type = "application/json; charset=utf-8"
        filename = f"export_{export_request.session_id}.json"
        
    elif format_lower == "excel":
        file_data = export_service.export_to_excel(export_request.session_id)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"export_{export_request.session_id}.xlsx"
        
    else:
        raise HTTPException(
            status_code=400,
            detail="Неподдерживаемый формат. Используйте: csv, json или excel"
        )
    
    # Возвращаем файл
    return Response(
        content=file_data.getvalue(),
        media_type=media_type,
        headers={
            "Content-Disposition": f"attachment; filename={filename}"
        }
    )


@router.get("/export/history", response_model=List[ExportHistoryResponse], tags=["Export"])
async def get_export_history(db: Session = Depends(get_db)):
    """
    Получить историю всех экспортов
    Возвращает информацию о ранее выполненных экспортах
    """
    history = db.query(ExportHistory).order_by(ExportHistory.created_at.desc()).all()
    return history


@router.get("/export/history/{session_id}", response_model=List[ExportHistoryResponse], tags=["Export"])
async def get_session_export_history(session_id: int, db: Session = Depends(get_db)):
    """
    Получить историю экспортов для конкретной сессии
    
    Args:
        session_id: ID парсинг-сессии
    
    Returns:
        Список экспортов для указанной сессии
    """
    history = db.query(ExportHistory).filter(
        ExportHistory.session_id == session_id
    ).order_by(ExportHistory.created_at.desc()).all()
    
    return history