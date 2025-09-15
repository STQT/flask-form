#!/usr/bin/env python3
"""
Скрипт для настройки Google Sheets API
"""

import os
import json
from google.oauth2.service_account import Credentials
import gspread

def setup_google_sheets():
    """Настройка Google Sheets API"""
    
    print("🔧 Настройка Google Sheets API")
    print("=" * 50)
    
    # Проверяем наличие файла credentials.json
    if not os.path.exists('credentials.json'):
        print("❌ Файл credentials.json не найден!")
        print("\n📋 Инструкции по созданию файла credentials.json:")
        print("1. Перейдите в Google Cloud Console: https://console.cloud.google.com/")
        print("2. Создайте новый проект или выберите существующий")
        print("3. Включите Google Sheets API и Google Drive API")
        print("4. Создайте Service Account:")
        print("   - Перейдите в IAM & Admin > Service Accounts")
        print("   - Нажмите 'Create Service Account'")
        print("   - Заполните название и описание")
        print("   - Нажмите 'Create and Continue'")
        print("   - В ролях выберите 'Editor'")
        print("   - Нажмите 'Done'")
        print("5. Создайте ключ для Service Account:")
        print("   - Найдите созданный Service Account в списке")
        print("   - Нажмите на него")
        print("   - Перейдите на вкладку 'Keys'")
        print("   - Нажмите 'Add Key' > 'Create new key'")
        print("   - Выберите 'JSON' и нажмите 'Create'")
        print("   - Скачайте файл и переименуйте его в 'credentials.json'")
        print("   - Поместите файл в корень проекта")
        return False
    
    try:
        # Проверяем подключение к Google Sheets
        print("🔍 Проверка подключения к Google Sheets...")
        
        SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
        client = gspread.authorize(creds)
        
        print("✅ Подключение к Google Sheets успешно!")
        
        # Создаем новую таблицу
        print("\n📊 Создание новой таблицы...")
        spreadsheet = client.create('Instagram Leads')
        
        # Настраиваем доступ
        spreadsheet.share('', perm_type='anyone', role='writer')
        
        print(f"✅ Таблица создана: {spreadsheet.url}")
        print(f"📋 ID таблицы: {spreadsheet.id}")
        
        # Настраиваем заголовки
        worksheet = spreadsheet.sheet1
        worksheet.update('A1:C1', [['Дата и время', 'Имя', 'Телефон']])
        
        # Форматируем заголовки
        worksheet.format('A1:C1', {
            'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9},
            'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
        })
        
        print("✅ Заголовки настроены!")
        
        # Создаем .env файл
        env_content = f"""# Google Sheets Configuration
GOOGLE_SHEET_ID={spreadsheet.id}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
"""
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Файл .env создан!")
        
        print("\n🎉 Настройка завершена!")
        print(f"📱 Ваша форма доступна по адресу: http://localhost:5000")
        print(f"📊 Данные будут сохраняться в таблице: {spreadsheet.url}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при настройке: {e}")
        return False

if __name__ == "__main__":
    setup_google_sheets()
