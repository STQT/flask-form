# 🐳 Docker Deployment для InterAutoSchool

## 🚀 Быстрый старт

### 1. Подготовка

```bash
# 1. Скопируйте файл с переменными окружения
cp env.production.example .env

# 2. Отредактируйте .env файл
nano .env

# 3. Убедитесь, что credentials.json существует
ls -la credentials.json
```

### 2. Запуск

```bash
# Автоматический деплой
./scripts/deploy.sh

# Или вручную
docker-compose -f docker-compose.prod.yml up -d
```

## 📋 Структура проекта

```
├── Dockerfile                 # Образ Flask приложения
├── docker-compose.yml         # Для разработки
├── docker-compose.prod.yml    # Для продакшна
├── nginx/
│   ├── nginx.conf            # Конфигурация Nginx
│   └── ssl/                  # SSL сертификаты
├── scripts/
│   ├── deploy.sh             # Скрипт деплоя
│   └── generate-ssl.sh       # Генерация SSL
├── monitoring/               # Мониторинг (Prometheus/Grafana)
└── logs/                     # Логи приложения
```

## 🔧 Конфигурация

### Переменные окружения (.env)

```env
# Flask
SECRET_KEY=your-super-secret-key
FLASK_ENV=production

# Google Sheets
GOOGLE_SHEET_ID=your_spreadsheet_id

# Email
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
TO_EMAIL=your-email@gmail.com

# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 🐳 Docker сервисы

### 1. **web** - Flask приложение
- **Порт:** 8000
- **Образ:** Собранный из Dockerfile
- **Переменные:** Из .env файла
- **Volumes:** credentials.json, logs, data

### 2. **nginx** - Reverse Proxy
- **Порты:** 80 (HTTP), 443 (HTTPS)
- **Функции:** SSL терминация, статические файлы, сжатие
- **Безопасность:** HSTS, XSS защита, заголовки безопасности

### 3. **redis** - Кеширование
- **Порт:** 6379
- **Функции:** Сессии, кеш, очереди задач

### 4. **prometheus** - Мониторинг (опционально)
- **Порт:** 9090
- **Функции:** Сбор метрик, алерты

### 5. **grafana** - Дашборды (опционально)
- **Порт:** 3000
- **Логин:** admin/admin
- **Функции:** Визуализация метрик

## 🚀 Команды

### Основные команды

```bash
# Запуск в продакшне
docker-compose -f docker-compose.prod.yml up -d

# Остановка
docker-compose -f docker-compose.prod.yml down

# Перезапуск
docker-compose -f docker-compose.prod.yml restart

# Просмотр логов
docker-compose -f docker-compose.prod.yml logs -f

# Обновление
docker-compose -f docker-compose.prod.yml pull
docker-compose -f docker-compose.prod.yml up -d
```

### Управление сервисами

```bash
# Запуск только Flask
docker-compose -f docker-compose.prod.yml up -d web

# Запуск с мониторингом
docker-compose -f docker-compose.prod.yml up -d web nginx redis prometheus grafana

# Просмотр статуса
docker-compose -f docker-compose.prod.yml ps
```

## 🔐 SSL сертификаты

### Для разработки (самоподписанный)

```bash
./scripts/generate-ssl.sh
```

### Для продакшна (Let's Encrypt)

```bash
# Установите certbot
sudo apt install certbot

# Получите сертификат
sudo certbot certonly --standalone -d yourdomain.com

# Скопируйте сертификаты
sudo cp /etc/letsencrypt/live/yourdomain.com/fullchain.pem nginx/ssl/cert.pem
sudo cp /etc/letsencrypt/live/yourdomain.com/privkey.pem nginx/ssl/key.pem
```

## 📊 Мониторинг

### Доступ к сервисам

- **Приложение:** https://yourdomain.com
- **Grafana:** http://yourdomain.com:3000 (admin/admin)
- **Prometheus:** http://yourdomain.com:9090
- **Health Check:** https://yourdomain.com/health

### Логи

```bash
# Все логи
docker-compose -f docker-compose.prod.yml logs

# Логи конкретного сервиса
docker-compose -f docker-compose.prod.yml logs web
docker-compose -f docker-compose.prod.yml logs nginx

# Следить за логами в реальном времени
docker-compose -f docker-compose.prod.yml logs -f web
```

## 🔧 Обслуживание

### Обновление приложения

```bash
# 1. Остановите сервисы
docker-compose -f docker-compose.prod.yml down

# 2. Обновите код
git pull origin main

# 3. Пересоберите образы
docker-compose -f docker-compose.prod.yml build --no-cache

# 4. Запустите заново
docker-compose -f docker-compose.prod.yml up -d
```

### Резервное копирование

```bash
# Создайте бэкап данных
tar -czf backup-$(date +%Y%m%d).tar.gz data/ logs/ credentials.json .env

# Восстановите из бэкапа
tar -xzf backup-20240115.tar.gz
```

## 🚨 Устранение неполадок

### Проблемы с запуском

```bash
# Проверьте статус контейнеров
docker-compose -f docker-compose.prod.yml ps

# Проверьте логи
docker-compose -f docker-compose.prod.yml logs web

# Проверьте конфигурацию
docker-compose -f docker-compose.prod.yml config
```

### Проблемы с SSL

```bash
# Проверьте сертификаты
openssl x509 -in nginx/ssl/cert.pem -text -noout

# Проверьте конфигурацию Nginx
docker-compose -f docker-compose.prod.yml exec nginx nginx -t
```

## 📈 Производительность

### Оптимизация

- **Workers:** Настроено 4 воркера Gunicorn
- **Nginx:** Включено сжатие gzip
- **Redis:** Кеширование для быстрого доступа
- **Health checks:** Автоматический перезапуск при сбоях

### Масштабирование

```bash
# Увеличьте количество воркеров
docker-compose -f docker-compose.prod.yml up -d --scale web=3
```

## 🎉 Готово!

Ваше приложение готово к продакшну! 

**Доступно по адресу:** https://yourdomain.com
**UTM тест:** https://yourdomain.com/utm-test
