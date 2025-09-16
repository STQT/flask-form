# 🕐 Обновление часового пояса на Asia/Tashkent

## ✅ Что изменено

### 1. **Добавлена поддержка часового пояса Asia/Tashkent**
- Добавлен импорт `pytz` для работы с часовыми поясами
- Создана функция `get_tashkent_time()` для получения времени в часовом поясе Asia/Tashkent
- Заменены все использования `datetime.now()` на `get_tashkent_time()`

### 2. **Обновлены файлы:**
- ✅ **`app.py`** - основная логика приложения
- ✅ **`requirements.txt`** - добавлена библиотека `pytz==2024.1`

### 3. **Места где применяется новое время:**
- 📊 **Google Sheets** - время сохранения лидов
- 📧 **Email уведомления** - время в теме и теле письма
- 📱 **Telegram уведомления** - время в сообщениях
- 💾 **CSV файлы** - время сохранения (если используется)

## 🌍 Часовой пояс

**Asia/Tashkent** = UTC +5 часов

### Примеры времени:
- **UTC:** 06:44:47
- **Tashkent:** 11:44:47 (+5 часов)

## 🚀 Как использовать

### 1. **Установка зависимостей:**
```bash
source venv/bin/activate
pip install pytz==2024.1
```

### 2. **Запуск приложения:**
```bash
source venv/bin/activate
python app.py
```

### 3. **Docker (продакшн):**
```bash
# Образ автоматически обновится с новыми зависимостями
docker-compose -f docker-compose.prod.yml up -d
```

## 📋 Проверка

Время в Google Sheets теперь будет отображаться в часовом поясе **Asia/Tashkent** вместо UTC.

### Тест:
1. Откройте форму: http://localhost:8000/
2. Заполните и отправьте форму
3. Проверьте время в Google Sheets - должно быть на +5 часов от UTC

## 🔧 Технические детали

### Функция `get_tashkent_time()`:
```python
def get_tashkent_time():
    """Получение текущего времени в часовом поясе Asia/Tashkent"""
    tashkent_tz = pytz.timezone('Asia/Tashkent')
    return datetime.now(tashkent_tz)
```

### Использование:
```python
# Вместо:
timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Теперь:
timestamp = get_tashkent_time().strftime('%Y-%m-%d %H:%M:%S')
```

## ✅ Результат

Теперь все временные метки в приложении будут отображаться в часовом поясе **Asia/Tashkent (UTC+5)**, что соответствует местному времени в Узбекистане.

