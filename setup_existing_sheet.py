#!/usr/bin/env python3
"""
Настройка с существующей Google Sheets таблицей
"""

import gspread
from google.oauth2.service_account import Credentials
import os

def setup_existing_sheet():
    """Настройка с существующей таблицей"""
    
    print("🔧 Настройка с существующей Google Sheets таблицей")
    print("=" * 60)
    
    # Проверяем наличие файла credentials.json
    if not os.path.exists('credentials.json'):
        print("❌ Файл credentials.json не найден!")
        print("\n📋 Создайте Service Account и скачайте credentials.json:")
        print("1. Перейдите в Google Cloud Console")
        print("2. Создайте Service Account")
        print("3. Скачайте JSON ключ как 'credentials.json'")
        return False
    
    try:
        # Подключаемся к Google Sheets
        SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
        ]
        
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
        client = gspread.authorize(creds)
        
        print("✅ Подключение к Google Sheets успешно!")
        
        # Список существующих таблиц
        print("\n📊 Ваши Google Sheets таблицы:")
        try:
            spreadsheets = client.list_spreadsheet_files()
            for i, sheet in enumerate(spreadsheets[:10], 1):  # Показываем первые 10
                print(f"{i}. {sheet['name']} (ID: {sheet['id']})")
        except Exception as e:
            print(f"⚠️ Не удалось получить список таблиц: {e}")
        
        # Запрашиваем ID существующей таблицы
        print("\n📝 Введите ID существующей таблицы:")
        print("(ID можно найти в URL: https://docs.google.com/spreadsheets/d/ID_ТАБЛИЦЫ/edit)")
        
        spreadsheet_id = input("ID таблицы: ").strip()
        
        if not spreadsheet_id:
            print("❌ ID таблицы не указан!")
            return False
        
        # Проверяем доступ к таблице
        try:
            spreadsheet = client.open_by_key(spreadsheet_id)
            print(f"✅ Доступ к таблице '{spreadsheet.title}' получен!")
            
            # Настраиваем заголовки
            worksheet = spreadsheet.sheet1
            worksheet.update('A1:H1', [['Дата и время', 'Имя', 'Телефон', 'UTM Source', 'UTM Medium', 'UTM Campaign', 'UTM Term', 'UTM Content']])
            
            # Форматируем заголовки
            worksheet.format('A1:H1', {
                'backgroundColor': {'red': 0.2, 'green': 0.6, 'blue': 0.9},
                'textFormat': {'bold': True, 'foregroundColor': {'red': 1, 'green': 1, 'blue': 1}}
            })
            
            print("✅ Заголовки настроены!")
            
            # Создаем .env файл
            env_content = f"""# Google Sheets Configuration
GOOGLE_SHEET_ID={spreadsheet_id}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
"""
            
            with open('.env', 'w', encoding='utf-8') as f:
                f.write(env_content)
            
            print("✅ Файл .env создан!")
            
            print(f"\n🎉 Настройка завершена!")
            print(f"📱 Ваша форма доступна по адресу: http://localhost:8000")
            print(f"📊 Данные будут сохраняться в таблице: {spreadsheet.url}")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка доступа к таблице: {e}")
            print("💡 Убедитесь, что:")
            print("   - ID таблицы правильный")
            print("   - Service Account имеет доступ к таблице")
            print("   - Таблица не удалена")
            return False
        
    except Exception as e:
        print(f"❌ Ошибка при настройке: {e}")
        return False

if __name__ == "__main__":
    setup_existing_sheet()
