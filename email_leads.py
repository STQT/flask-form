#!/usr/bin/env python3
"""
Альтернативный метод отправки лидов на email
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os

def send_lead_email(name, phone, to_email="your-email@gmail.com"):
    """Отправка лида на email"""
    
    # Настройки SMTP (Gmail)
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
    sender_password = os.getenv('SENDER_PASSWORD', 'your-app-password')
    
    # Создаем сообщение
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = f"Новый лид от InterAutoSchool - {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    
    # Тело письма
    body = f"""
    🚗 Новый лид от InterAutoSchool
    
    📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
    👤 Имя: {name}
    📞 Телефон: {phone}
    
    ---
    Отправлено автоматически с формы InterAutoSchool
    """
    
    msg.attach(MIMEText(body, 'plain', 'utf-8'))
    
    try:
        # Подключаемся к серверу
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        
        # Отправляем письмо
        text = msg.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        
        print(f"✅ Лид отправлен на {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Ошибка отправки email: {e}")
        return False

if __name__ == "__main__":
    # Тестовая отправка
    send_lead_email("Тест Тестов", "+998 99 123-45-67")
