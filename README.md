# ExportService - Сервис экспорта результатов парсинга

Микросервис для экспорта данных парсинга в форматы CSV, JSON и Excel.

## 📋 Описание

ExportService - это микросервис, который получает готовые данные из базы после завершенной парсинг-сессии и предоставляет возможность экспортировать их в различных форматах.

### Основные возможности:
- ✅ Экспорт данных в форматы CSV, JSON, Excel
- ✅ Просмотр доступных парсинг-сессий
- ✅ Предпросмотр данных перед экспортом
- ✅ История экспортов
- ✅ REST API для интеграции
- ✅ Веб-интерфейс для удобной работы

## 🛠 Технологический стек

### Backend:
- **FastAPI** - современный веб-фреймворк для Python
- **PostgreSQL** - реляционная база данных
- **SQLAlchemy** - ORM для работы с БД
- **Pandas** - обработка и экспорт данных
- **Pydantic** - валидация данных

### Frontend:
- **HTML/CSS/JavaScript** - простой и понятный интерфейс
- **Nginx** - веб-сервер для статики

### DevOps:
- **Docker** - контейнеризация
- **Docker Compose** - оркестрация контейнеров

## 🚀 Быстрый старт

### Предварительные требования:
- Docker и Docker Compose
- Git

### Установка и запуск:

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd export-service
```

2. Создайте файл `.env` на основе `.env.example`:
```bash
cp backend/.env.example backend/.env
```

3. Запустите сервисы через Docker Compose:
```bash
docker-compose up -d
```

4. Дождитесь запуска всех контейнеров (около 30 секунд)

5. Откройте в браузере:
   - **Веб-интерфейс**: http://localhost:3000
   - **API документация**: http://localhost:8000/docs
   - **ReDoc**: http://localhost:8000/redoc

## 📚 API Endpoints

### Основные endpoints:

#### Проверка работоспособности сервиса
```http
GET /api/v1/health
```

#### Получить список сессий
```http
GET /api/v1/sessions
```

#### Получить данные сессии
```http
GET /api/v1/sessions/{session_id}
```

#### Экспортировать данные
```http
POST /api/v1/export
Content-Type: application/json

{
  "session_id": 1,
  "format": "csv"  // csv, json, excel
}
```

#### История экспортов
```http
GET /api/v1/export/history
GET /api/v1/export/history/{session_id}
```

## 🗄 Структура базы данных

### Таблица `parsing_sessions`
Хранит информацию о парсинг-сессиях:
- `id` - уникальный идентификатор
- `session_name` - название сессии
- `status` - статус (completed, in_progress)
- `created_at` - дата создания
- `completed_at` - дата завершения
- `total_items` - количество элементов

### Таблица `parsed_data`
Хранит спарсенные данные о товарах:
- `id` - уникальный идентификатор
- `session_id` - ссылка на сессию
- `product_name` - название товара
- `price` - цена
- `old_price` - старая цена
- `currency` - валюта
- `description` - описание
- `category` - категория
- `in_stock` - наличие
- `url` - ссылка на товар
- `image_url` - ссылка на изображение
- `brand` - бренд
- `created_at` - дата добавления

### Таблица `export_history`
Хранит историю экспортов:
- `id` - уникальный идентификатор
- `session_id` - ссылка на сессию
- `export_format` - формат экспорта
- `file_name` - имя файла
- `file_size` - размер файла
- `records_count` - количество записей
- `created_at` - дата экспорта

## 📁 Структура проекта

```
export-service/
├── backend/                 # Backend приложение
│   ├── app/
│   │   ├── api/            # API endpoints
│   │   ├── core/           # Конфигурация
│   │   ├── database/       # Подключение к БД
│   │   ├── models/         # Модели данных
│   │   ├── schemas/        # Pydantic схемы
│   │   ├── services/       # Бизнес-логика
│   │   └── main.py         # Точка входа
│   ├── requirements.txt    # Python зависимости
│   ├── Dockerfile          # Docker образ
│   ├── init.sql           # Инициализация БД
│   └── .env.example       # Пример конфигурации
├── frontend/               # Frontend приложение
│   ├── index.html         # Главная страница
│   ├── styles.css         # Стили
│   ├── script.js          # JavaScript логика
│   └── nginx.conf         # Конфигурация Nginx
├── docs/                   # Документация
├── tests/                  # Тесты
└── docker-compose.yml     # Оркестрация контейнеров
```

## 🧪 Тестирование

### Запуск через Postman:
1. Импортируйте коллекцию из `tests/ExportService.postman_collection.json`
2. Запустите тесты

### Ручное тестирование:
```bash
# Проверка здоровья
curl http://localhost:8000/api/v1/health

# Получение сессий
curl http://localhost:8000/api/v1/sessions

# Экспорт в CSV
curl -X POST http://localhost:8000/api/v1/export \
  -H "Content-Type: application/json" \
  -d '{"session_id": 1, "format": "csv"}' \
  --output export.csv
```

## 🔧 Разработка

### Локальный запуск без Docker:

1. Установите зависимости:
```bash
cd backend
pip install -r requirements.txt
```

2. Настройте переменные окружения в `.env`

3. Запустите PostgreSQL

4. Запустите приложение:
```bash
uvicorn app.main:app --reload
```

## 📊 Мониторинг и логи

### Просмотр логов:
```bash
# Все сервисы
docker-compose logs -f

# Только backend
docker-compose logs -f backend

# Только база данных
docker-compose logs -f postgres
```

### Остановка сервисов:
```bash
docker-compose down
```

### Полная очистка (включая данные):
```bash
docker-compose down -v
```

## 🤝 Интеграция с другими сервисами

ExportService разработан как независимый микросервис и может работать автономно. Для интеграции с другими сервисами проекта Parser:

1. Используйте REST API для получения данных
2. Настройте общую сеть Docker для взаимодействия между сервисами
3. Используйте общую базу данных или настройте репликацию

## 📝 Автор

**Мамыкин Всеволод**  
Студент группы ИУ6-65Б  
МГТУ им. Н.Э. Баумана

## 📄 Лицензия

Проект разработан в рамках учебного курса "Инженерия требований и спецификация программного обеспечения"
