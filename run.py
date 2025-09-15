#!/usr/bin/env python3
"""
Скрипт для запуска приложения
"""

import os
import sys
from app import app

if __name__ == "__main__":
    # Проверяем наличие необходимых файлов
    if not os.path.exists('credentials.json'):
        print("❌ Файл credentials.json не найден!")
        print("📋 Запустите: python setup_google_sheets.py")
        sys.exit(1)
    
    if not os.path.exists('.env'):
        print("❌ Файл .env не найден!")
        print("📋 Запустите: python setup_google_sheets.py")
        sys.exit(1)
    
    print("🚀 Запуск Instagram Leads Form...")
    print("📱 Форма доступна по адресу: http://localhost:8000")
    print("🛑 Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    app.run(debug=True, host='0.0.0.0', port=8000)
