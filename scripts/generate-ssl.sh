#!/bin/bash

# Генерация самоподписанного SSL сертификата для разработки
# В продакшне используйте Let's Encrypt или купленный сертификат

echo "🔐 Генерация SSL сертификата..."

# Создаем директорию для SSL
mkdir -p nginx/ssl

# Генерируем приватный ключ
openssl genrsa -out nginx/ssl/key.pem 2048

# Генерируем сертификат
openssl req -new -x509 -key nginx/ssl/key.pem -out nginx/ssl/cert.pem -days 365 -subj "/C=UZ/ST=Tashkent/L=Tashkent/O=InterAutoSchool/OU=IT/CN=localhost"

echo "✅ SSL сертификат создан в nginx/ssl/"
echo "⚠️  Это самоподписанный сертификат для разработки"
echo "📋 Для продакшна используйте Let's Encrypt:"
echo "   certbot certonly --standalone -d yourdomain.com"
