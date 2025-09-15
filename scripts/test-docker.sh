#!/bin/bash

# Тестирование Docker конфигурации

echo "🧪 Тестируем Docker конфигурацию..."

# Проверяем наличие Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker не установлен!"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose не установлен!"
    exit 1
fi

# Проверяем конфигурацию
echo "🔍 Проверяем конфигурацию..."
docker-compose -f docker-compose.prod.yml config

# Собираем образ
echo "🔨 Собираем образ..."
docker-compose -f docker-compose.prod.yml build

# Запускаем тест
echo "🚀 Запускаем тест..."
docker-compose -f docker-compose.prod.yml up -d

# Ждем запуска
echo "⏳ Ждем запуска..."
sleep 10

# Проверяем статус
echo "📊 Статус сервисов:"
docker-compose -f docker-compose.prod.yml ps

# Тестируем приложение
echo "🌐 Тестируем приложение..."
if curl -f http://localhost:8000/ > /dev/null 2>&1; then
    echo "✅ Приложение работает!"
else
    echo "❌ Ошибка приложения!"
fi

# Останавливаем
echo "🛑 Останавливаем тест..."
docker-compose -f docker-compose.prod.yml down

echo "🎉 Тест завершен!"
