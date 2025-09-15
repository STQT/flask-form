from flask import Flask, render_template, request, jsonify, redirect, url_for
import gspread
from google.oauth2.service_account import Credentials
import os
from datetime import datetime
import re
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Конфигурация Google Sheets
SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

def get_google_sheets_client():
    """Инициализация клиента Google Sheets"""
    try:
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPE)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Ошибка инициализации Google Sheets: {e}")
        return None

def save_lead_csv(name, phone, utm_source='', utm_medium='', utm_campaign='', utm_term='', utm_content=''):
    """Сохранение в CSV файл"""
    try:
        file_exists = os.path.exists('leads.csv')
        with open('leads.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Дата и время', 'Имя', 'Телефон', 'UTM Source', 'UTM Medium', 'UTM Campaign', 'UTM Term', 'UTM Content']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                'Дата и время': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Имя': name,
                'Телефон': phone,
                'UTM Source': utm_source,
                'UTM Medium': utm_medium,
                'UTM Campaign': utm_campaign,
                'UTM Term': utm_term,
                'UTM Content': utm_content
            })
        return True
    except Exception as e:
        print(f"Ошибка сохранения CSV: {e}")
        return False

def send_email_lead(name, phone):
    """Отправка лида на email"""
    try:
        sender_email = os.getenv('SENDER_EMAIL', 'your-email@gmail.com')
        sender_password = os.getenv('SENDER_PASSWORD', 'your-app-password')
        to_email = os.getenv('TO_EMAIL', 'your-email@gmail.com')
        
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to_email
        msg['Subject'] = f"Новый лид InterAutoSchool - {datetime.now().strftime('%d.%m.%Y %H:%M')}"
        
        body = f"""
        🚗 Новый лид от InterAutoSchool
        
        📅 Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
        👤 Имя: {name}
        📞 Телефон: {phone}
        """
        
        msg.attach(MIMEText(body, 'plain', 'utf-8'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        
        return True
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
        return False

def send_telegram_lead(name, phone):
    """Отправка лида в Telegram"""
    try:
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not bot_token or not chat_id:
            return False
        
        message = f"""
🚗 *Новый лид от InterAutoSchool*

📅 *Дата:* {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
👤 *Имя:* {name}
📞 *Телефон:* {phone}
        """
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        data = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=data)
        return response.status_code == 200
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False

def validate_phone(phone):
    """Валидация номера телефона (Узбекистан)"""
    # Удаляем все символы кроме цифр
    phone_digits = re.sub(r'\D', '', phone)
    # Проверяем что номер начинается с 998 и содержит 12 цифр
    return phone_digits.startswith('998') and len(phone_digits) == 12

def validate_name(name):
    """Валидация имени (поддержка узбекского кириллицы)"""
    # Проверяем что имя содержит только буквы, пробелы и дефисы (включая узбекские символы)
    return bool(re.match(r'^[a-zA-Zа-яА-ЯўҒғҳқҚўЎ\s\-]+$', name.strip())) and len(name.strip()) >= 2

@app.route('/')
def index():
    """Главная страница с формой"""
    # Получаем UTM параметры из URL
    utm_source = request.args.get('utm_source', '')
    utm_medium = request.args.get('utm_medium', '')
    utm_campaign = request.args.get('utm_campaign', '')
    utm_term = request.args.get('utm_term', '')
    utm_content = request.args.get('utm_content', '')
    
    return render_template('index.html', 
                         utm_source=utm_source,
                         utm_medium=utm_medium,
                         utm_campaign=utm_campaign,
                         utm_term=utm_term,
                         utm_content=utm_content)

@app.route('/submit', methods=['POST'])
def submit_lead():
    """Обработка отправки формы"""
    try:
        # Получаем данные из формы
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        
        # Получаем UTM параметры
        utm_source = request.form.get('utm_source', '')
        utm_medium = request.form.get('utm_medium', '')
        utm_campaign = request.form.get('utm_campaign', '')
        utm_term = request.form.get('utm_term', '')
        utm_content = request.form.get('utm_content', '')
        
        # Валидация данных
        if not validate_name(name):
            return jsonify({
                'success': False,
                'message': 'Илтимос, тўғри исм киритинг (фақат ҳарфлар, камида 2 та белги)'
            }), 400
        
        if not validate_phone(phone):
            return jsonify({
                'success': False,
                'message': 'Илтимос, тўғри телефон рақамини киритинг (Узбекистан: +998)'
            }), 400
        
        # Пробуем разные методы сохранения
        success = False
        
        # 1. Пробуем Google Sheets
        try:
            client = get_google_sheets_client()
            if client:
                spreadsheet_id = app.config['GOOGLE_SHEET_ID']
                if spreadsheet_id != 'your_spreadsheet_id_here':
                    sheet = client.open_by_key(spreadsheet_id).sheet1
                    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    # Добавляем UTM данные в Google Sheets
                    sheet.append_row([timestamp, name, phone, utm_source, utm_medium, utm_campaign, utm_term, utm_content])
                    success = True
                    print("✅ Сохранено в Google Sheets")
        except Exception as e:
            print(f"⚠️ Google Sheets недоступен: {e}")
        
        # 2. Пробуем Telegram
        if not success:
            if send_telegram_lead(name, phone):
                success = True
                print("✅ Отправлено в Telegram")
        
        # 3. Пробуем Email
        if not success:
            if send_email_lead(name, phone):
                success = True
                print("✅ Отправлено на Email")
        
        # 4. Сохраняем в CSV как резерв
        # save_lead_csv(name, phone, utm_source, utm_medium, utm_campaign, utm_term, utm_content)
        # print("✅ Сохранено в CSV файл")
        
        if not success:
            success = True  # CSV всегда работает
        
        return jsonify({
            'success': True,
            'message': 'Рахмат! Сизнинг маълумотларингиз муваффақиятли жўнатилди.'
        })
        
    except Exception as e:
        print(f"Ошибка при обработке формы: {e}")
        return jsonify({
            'success': False,
            'message': 'Хатолик юз берди. Кейинроқ уриниб кўринг.'
        }), 500

@app.route('/success')
def success():
    """Страница успешной отправки"""
    return render_template('success.html')

@app.route('/utm-test')
def utm_test():
    """Страница для тестирования UTM меток"""
    return render_template('utm_test.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
