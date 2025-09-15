#!/bin/bash

# Скрипт для деплоя в продакшн

set -e

echo "🚀 Начинаем деплой InterAutoSchool..."

# Проверяем наличие необходимых файлов
if [ ! -f "credentials.json" ]; then
    echo "❌ Файл credentials.json не найден!"
    echo "📋 Создайте Service Account и скачайте credentials.json"
    exit 1
fi

if [ ! -f ".env" ]; then
    echo "❌ Файл .env не найден!"
    echo "📋 Скопируйте env.production.example в .env и заполните настройки"
    exit 1
fi

# Создаем необходимые директории
mkdir -p logs nginx/ssl data monitoring/grafana/dashboards monitoring/grafana/datasources

# Генерируем SSL сертификат (если не существует)
if [ ! -f "nginx/ssl/cert.pem" ]; then
    echo "🔐 Генерируем SSL сертификат..."
    ./scripts/generate-ssl.sh
fi

# Останавливаем старые контейнеры
echo "🛑 Останавливаем старые контейнеры..."
docker-compose -f docker-compose.prod.yml down

# Собираем новые образы
echo "🔨 Собираем Docker образы..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Запускаем сервисы
echo "🚀 Запускаем сервисы..."
docker-compose -f docker-compose.prod.yml up -d

# Ждем запуска
echo "⏳ Ждем запуска сервисов..."
sleep 30

# Проверяем статус
echo "📊 Проверяем статус сервисов..."
docker-compose -f docker-compose.prod.yml ps

# Проверяем health check
echo "🏥 Проверяем health check..."
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo "✅ Приложение успешно запущено!"
    echo "🌐 Доступно по адресу: https://localhost"
    echo "📊 Мониторинг: http://localhost:3000 (Grafana)"
    echo "📈 Метрики: http://localhost:9090 (Prometheus)"
else
    echo "❌ Ошибка запуска приложения!"
    echo "📋 Проверьте логи: docker-compose -f docker-compose.prod.yml logs"
    exit 1
fi

echo "🎉 Деплой завершен успешно!"
