-- Инициализация базы данных для ExportService

-- Таблица для хранения информации о парсинг-сессиях (заглушка)
CREATE TABLE IF NOT EXISTS parsing_sessions (
    id SERIAL PRIMARY KEY,
    session_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    total_items INTEGER DEFAULT 0
);

-- Таблица для хранения спарсенных данных (заглушка)
CREATE TABLE IF NOT EXISTS parsed_data (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES parsing_sessions(id) ON DELETE CASCADE,
    product_name VARCHAR(500),
    price DECIMAL(10, 2),
    old_price DECIMAL(10, 2),
    currency VARCHAR(10) DEFAULT 'RUB',
    description TEXT,
    category VARCHAR(255),
    in_stock BOOLEAN DEFAULT TRUE,
    url TEXT,
    image_url TEXT,
    brand VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Таблица для хранения истории экспортов
CREATE TABLE IF NOT EXISTS export_history (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES parsing_sessions(id) ON DELETE CASCADE,
    export_format VARCHAR(20) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_size INTEGER,
    records_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_parsed_data_session ON parsed_data(session_id);
CREATE INDEX IF NOT EXISTS idx_export_history_session ON export_history(session_id);
CREATE INDEX IF NOT EXISTS idx_parsing_sessions_status ON parsing_sessions(status);

-- Вставка тестовых данных для демонстрации
INSERT INTO parsing_sessions (session_name, status, completed_at, total_items) VALUES
    ('Тестовая сессия 1', 'completed', CURRENT_TIMESTAMP, 5),
    ('Тестовая сессия 2', 'completed', CURRENT_TIMESTAMP - INTERVAL '1 day', 3);

INSERT INTO parsed_data (session_id, product_name, price, old_price, currency, description, category, in_stock, url, brand) VALUES
    (1, 'iPhone 15 Pro', 99990.00, 109990.00, 'RUB', 'Смартфон Apple iPhone 15 Pro 256GB', 'Электроника', TRUE, 'https://example.com/iphone15', 'Apple'),
    (1, 'Samsung Galaxy S24', 89990.00, 94990.00, 'RUB', 'Смартфон Samsung Galaxy S24 256GB', 'Электроника', TRUE, 'https://example.com/galaxy-s24', 'Samsung'),
    (1, 'MacBook Pro 14', 189990.00, 199990.00, 'RUB', 'Ноутбук Apple MacBook Pro 14 M3', 'Компьютеры', TRUE, 'https://example.com/macbook', 'Apple'),
    (1, 'AirPods Pro 2', 24990.00, 27990.00, 'RUB', 'Наушники Apple AirPods Pro 2', 'Аксессуары', TRUE, 'https://example.com/airpods', 'Apple'),
    (1, 'iPad Air', 64990.00, 69990.00, 'RUB', 'Планшет Apple iPad Air 11', 'Планшеты', FALSE, 'https://example.com/ipad', 'Apple'),
    (2, 'Sony WH-1000XM5', 29990.00, 34990.00, 'RUB', 'Наушники Sony WH-1000XM5', 'Аксессуары', TRUE, 'https://example.com/sony-headphones', 'Sony'),
    (2, 'Dell XPS 15', 149990.00, NULL, 'RUB', 'Ноутбук Dell XPS 15', 'Компьютеры', TRUE, 'https://example.com/dell-xps', 'Dell'),
    (2, 'Logitech MX Master 3S', 8990.00, 9990.00, 'RUB', 'Мышь Logitech MX Master 3S', 'Аксессуары', TRUE, 'https://example.com/logitech-mouse', 'Logitech');