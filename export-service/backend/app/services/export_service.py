"""
Сервис для экспорта данных в различные форматы
Поддерживает CSV, JSON и Excel форматы
"""

import pandas as pd
import json
from io import BytesIO
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models.models import ParsedData, ExportHistory
from datetime import datetime


class ExportService:
    """Класс для экспорта данных парсинга"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def _get_data_for_export(self, session_id: int) -> List[Dict[str, Any]]:
        """
        Получает данные из БД для экспорта
        
        Args:
            session_id: ID парсинг-сессии
            
        Returns:
            Список словарей с данными товаров
        """
        # Получаем все данные по сессии
        parsed_items = self.db.query(ParsedData).filter(
            ParsedData.session_id == session_id
        ).all()
        
        # Преобразуем в список словарей
        data = []
        for item in parsed_items:
            data.append({
                'ID': item.id,
                'Название товара': item.product_name,
                'Цена': float(item.price) if item.price else None,
                'Старая цена': float(item.old_price) if item.old_price else None,
                'Валюта': item.currency,
                'Описание': item.description,
                'Категория': item.category,
                'В наличии': 'Да' if item.in_stock else 'Нет',
                'URL': item.url,
                'Изображение': item.image_url,
                'Бренд': item.brand,
                'Дата добавления': item.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        
        return data
    
    def export_to_csv(self, session_id: int) -> BytesIO:
        """
        Экспортирует данные в CSV формат
        
        Args:
            session_id: ID парсинг-сессии
            
        Returns:
            BytesIO объект с CSV данными
        """
        data = self._get_data_for_export(session_id)
        
        # Создаем DataFrame
        df = pd.DataFrame(data)
        
        # Экспортируем в CSV
        output = BytesIO()
        df.to_csv(output, index=False, encoding='utf-8-sig')  # utf-8-sig для корректного отображения в Excel
        output.seek(0)
        
        # Сохраняем информацию об экспорте
        self._save_export_history(
            session_id=session_id,
            export_format='csv',
            file_name=f'export_{session_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            file_size=output.getbuffer().nbytes,
            records_count=len(data)
        )
        
        return output
    
    def export_to_json(self, session_id: int) -> BytesIO:
        """
        Экспортирует данные в JSON формат
        
        Args:
            session_id: ID парсинг-сессии
            
        Returns:
            BytesIO объект с JSON данными
        """
        data = self._get_data_for_export(session_id)
        
        # Экспортируем в JSON
        output = BytesIO()
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        output.write(json_str.encode('utf-8'))
        output.seek(0)
        
        # Сохраняем информацию об экспорте
        self._save_export_history(
            session_id=session_id,
            export_format='json',
            file_name=f'export_{session_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
            file_size=output.getbuffer().nbytes,
            records_count=len(data)
        )
        
        return output
    
    def export_to_excel(self, session_id: int) -> BytesIO:
        """
        Экспортирует данные в Excel формат с автоподбором ширины колонок
        
        Args:
            session_id: ID парсинг-сессии
            
        Returns:
            BytesIO объект с Excel данными
        """
        data = self._get_data_for_export(session_id)
        
        # Создаем DataFrame
        df = pd.DataFrame(data)
        
        # Используем BytesIO для работы с файлом в памяти
        output = BytesIO()
        
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, sheet_name='Данные парсинга', index=False)
            
            # Получаем worksheet для настройки ширины колонок
            worksheet = writer.sheets['Данные парсинга']
            
            # Автоподбор ширины колонок
            for idx, col in enumerate(df.columns):
                # Находим максимальную длину: max(длина_значений, длина_заголовка)
                max_len = max(
                    df[col].astype(str).apply(len).max(),
                    len(col)
                ) + 2
                # Ограничиваем максимум 50 символами
                worksheet.set_column(idx, idx, min(max_len, 50))
        
        # Перемещаем указатель в начало потока
        output.seek(0)
        
        # Сохраняем информацию об экспорте
        self._save_export_history(
            session_id=session_id,
            export_format='excel',
            file_name=f'export_{session_id}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            file_size=output.getbuffer().nbytes,
            records_count=len(data)
        )
        
        return output
    
    def _save_export_history(self, session_id: int, export_format: str, 
                            file_name: str, file_size: int, records_count: int):
        """
        Сохраняет информацию об экспорте в историю
        
        Args:
            session_id: ID парсинг-сессии
            export_format: Формат экспорта
            file_name: Имя файла
            file_size: Размер файла в байтах
            records_count: Количество записей
        """
        export_record = ExportHistory(
            session_id=session_id,
            export_format=export_format,
            file_name=file_name,
            file_size=file_size,
            records_count=records_count
        )
        self.db.add(export_record)
        self.db.commit()