// JavaScript для работы с ExportService API

// Конфигурация API
const API_BASE_URL = 'http://localhost:8000/api/v1';

// Глобальные переменные
let sessions = [];
let selectedSessionId = null;

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', () => {
    loadSessions();
    loadExportHistory();
    setupEventListeners();
});

// Настройка обработчиков событий
function setupEventListeners() {
    const exportBtn = document.getElementById('export-btn');
    const sessionSelect = document.getElementById('session-select');
    
    exportBtn.addEventListener('click', handleExport);
    sessionSelect.addEventListener('change', handleSessionChange);
}

// Загрузка списка сессий
async function loadSessions() {
    try {
        const response = await fetch(`${API_BASE_URL}/sessions`);
        
        if (!response.ok) {
            throw new Error('Ошибка загрузки сессий');
        }
        
        sessions = await response.json();
        displaySessions(sessions);
        populateSessionSelect(sessions);
        
    } catch (error) {
        console.error('Ошибка:', error);
        showError('sessions-list', 'Не удалось загрузить список сессий');
    }
}

// Отображение сессий в виде карточек
function displaySessions(sessions) {
    const container = document.getElementById('sessions-list');
    
    if (sessions.length === 0) {
        container.innerHTML = '<p class="info-text">Нет доступных сессий</p>';
        return;
    }
    
    container.innerHTML = sessions.map(session => `
        <div class="session-item" data-session-id="${session.id}" onclick="selectSession(${session.id})">
            <div class="session-name">${session.session_name}</div>
            <div class="session-info">📊 Элементов: ${session.total_items}</div>
            <div class="session-info">📅 Создано: ${formatDate(session.created_at)}</div>
            <span class="session-status status-${session.status}">${getStatusText(session.status)}</span>
        </div>
    `).join('');
}

// Заполнение выпадающего списка сессий
function populateSessionSelect(sessions) {
    const select = document.getElementById('session-select');
    
    select.innerHTML = '<option value="">-- Выберите сессию --</option>' +
        sessions.map(session => 
            `<option value="${session.id}">${session.session_name} (${session.total_items} элементов)</option>`
        ).join('');
}

// Выбор сессии
function selectSession(sessionId) {
    selectedSessionId = sessionId;
    
    // Обновляем визуальное выделение
    document.querySelectorAll('.session-item').forEach(item => {
        item.classList.remove('selected');
    });
    document.querySelector(`[data-session-id="${sessionId}"]`).classList.add('selected');
    
    // Обновляем select
    document.getElementById('session-select').value = sessionId;
    
    // Загружаем данные для предпросмотра
    loadSessionData(sessionId);
}

// Обработка изменения выбора в select
function handleSessionChange(event) {
    const sessionId = parseInt(event.target.value);
    if (sessionId) {
        selectSession(sessionId);
    }
}

// Загрузка данных сессии для предпросмотра
async function loadSessionData(sessionId) {
    const container = document.getElementById('data-preview');
    container.innerHTML = '<p class="loading">Загрузка данных...</p>';
    
    try {
        const response = await fetch(`${API_BASE_URL}/sessions/${sessionId}`);
        
        if (!response.ok) {
            throw new Error('Ошибка загрузки данных');
        }
        
        const data = await response.json();
        displayDataPreview(data.parsed_data);
        
    } catch (error) {
        console.error('Ошибка:', error);
        showError('data-preview', 'Не удалось загрузить данные сессии');
    }
}

// Отображение предпросмотра данных
function displayDataPreview(data) {
    const container = document.getElementById('data-preview');
    
    if (!data || data.length === 0) {
        container.innerHTML = '<p class="info-text">Нет данных для отображения</p>';
        return;
    }
    
    // Показываем первые 10 записей
    const previewData = data.slice(0, 10);
    
    container.innerHTML = `
        <p class="info-text">Показано ${previewData.length} из ${data.length} записей</p>
        <table class="data-table">
            <thead>
                <tr>
                    <th>Название</th>
                    <th>Цена</th>
                    <th>Категория</th>
                    <th>Бренд</th>
                    <th>Наличие</th>
                </tr>
            </thead>
            <tbody>
                ${previewData.map(item => `
                    <tr>
                        <td>${item.product_name || '-'}</td>
                        <td>${item.price ? `${item.price} ${item.currency}` : '-'}</td>
                        <td>${item.category || '-'}</td>
                        <td>${item.brand || '-'}</td>
                        <td>${item.in_stock ? '✅ Да' : '❌ Нет'}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
}

// Обработка экспорта
async function handleExport() {
    const sessionId = document.getElementById('session-select').value;
    const format = document.getElementById('format-select').value;
    const statusDiv = document.getElementById('export-status');
    const exportBtn = document.getElementById('export-btn');
    
    if (!sessionId) {
        showStatus('Пожалуйста, выберите сессию', 'error');
        return;
    }
    
    // Блокируем кнопку
    exportBtn.disabled = true;
    showStatus('Экспорт данных...', 'info');
    
    try {
        const response = await fetch(`${API_BASE_URL}/export`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                session_id: parseInt(sessionId),
                format: format
            })
        });
        
        if (!response.ok) {
            throw new Error('Ошибка экспорта данных');
        }
        
        // Получаем файл
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `export_${sessionId}.${format === 'excel' ? 'xlsx' : format}`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
        
        showStatus('✅ Файл успешно экспортирован!', 'success');
        
        // Обновляем историю
        setTimeout(() => loadExportHistory(), 1000);
        
    } catch (error) {
        console.error('Ошибка:', error);
        showStatus('❌ Ошибка при экспорте данных', 'error');
    } finally {
        exportBtn.disabled = false;
    }
}

// Загрузка истории экспортов
async function loadExportHistory() {
    const container = document.getElementById('export-history');
    
    try {
        const response = await fetch(`${API_BASE_URL}/export/history`);
        
        if (!response.ok) {
            throw new Error('Ошибка загрузки истории');
        }
        
        const history = await response.json();
        displayExportHistory(history);
        
    } catch (error) {
        console.error('Ошибка:', error);
        showError('export-history', 'Не удалось загрузить историю экспортов');
    }
}

// Отображение истории экспортов
function displayExportHistory(history) {
    const container = document.getElementById('export-history');
    
    if (history.length === 0) {
        container.innerHTML = '<p class="info-text">История экспортов пуста</p>';
        return;
    }
    
    container.innerHTML = history.map(item => `
        <div class="history-item">
            <span class="history-format">${item.export_format.toUpperCase()}</span>
            <span class="history-info">
                📄 ${item.file_name} | 
                📊 ${item.records_count} записей | 
                💾 ${formatFileSize(item.file_size)} | 
                📅 ${formatDate(item.created_at)}
            </span>
        </div>
    `).join('');
}

// Вспомогательные функции

function showStatus(message, type) {
    const statusDiv = document.getElementById('export-status');
    statusDiv.textContent = message;
    statusDiv.className = `status-message show ${type}`;
    
    if (type === 'success') {
        setTimeout(() => {
            statusDiv.classList.remove('show');
        }, 5000);
    }
}

function showError(containerId, message) {
    const container = document.getElementById(containerId);
    container.innerHTML = `<p class="info-text" style="color: #d32f2f;">${message}</p>`;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatFileSize(bytes) {
    if (!bytes) return '-';
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
}

function getStatusText(status) {
    const statusMap = {
        'completed': 'Завершено',
        'in_progress': 'В процессе',
        'failed': 'Ошибка'
    };
    return statusMap[status] || status;
}