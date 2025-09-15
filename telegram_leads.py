#!/usr/bin/env python3
"""
Отправка лидов в Telegram
"""

import requests
import os
from datetime import datetime

def send_telegram_lead(name, phone, bot_token=None, chat_id=None):
    """Отправка лида в Telegram"""
    
    if not bot_token or not chat_id:
        print("❌ Не указаны bot_token или chat_id")
        return False
    
    message = f"""
🚗 *Новый лид от InterAutoSchool*

📅 *Дата:* {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
👤 *Имя:* {name}
📞 *Телефон:* {phone}

---
_Отправлено автоматически с формы InterAutoSchool_
    """
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    
    data = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown'
    }
    
    try:
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("✅ Лид отправлен в Telegram")
            return True
        else:
            print(f"❌ Ошибка отправки в Telegram: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def setup_telegram():
    """Настройка Telegram бота"""
    print("🤖 Настройка Telegram бота")
    print("=" * 40)
    
    print("1. Создайте бота через @BotFather в Telegram")
    print("2. Получите токен бота")
    print("3. Узнайте ID чата (отправьте /start боту и перейдите по ссылке)")
    print("   https://api.telegram.org/bot<TOKEN>/getUpdates")
    
    bot_token = input("\nВведите токен бота: ").strip()
    chat_id = input("Введите ID чата: ").strip()
    
    if bot_token and chat_id:
        # Создаем .env файл
        env_content = f"""# Telegram Configuration
TELEGRAM_BOT_TOKEN={bot_token}
TELEGRAM_CHAT_ID={chat_id}

# Flask Configuration
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-change-this-in-production
"""
        
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Настройка завершена!")
        return True
    else:
        print("❌ Не указаны токен или ID чата")
        return False

if __name__ == "__main__":
    setup_telegram()
