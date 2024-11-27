import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(smtp_server, smtp_port, sender, recipient, fake_from, subject, body):

    msg = MIMEMultipart()
    msg['From'] = fake_from 
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.sendmail(sender, recipient, msg.as_string())
            print(f"Письмо успешно отправлено на {recipient} от имени {fake_from}")
    except Exception as e:
        print(f"Ошибка отправки письма: {e}")


smtp_server = "127.0.0.1" 
smtp_port = 1025           
sender = "savinov.ii@phystech.edu"  # Настоящий адрес отправителя
recipient = "bulatova.aygul.2004@gmail.com" # Получатель
fake_from = "vansavinoff@yandex.ru" # Подменный адрес
subject = "Привет"
body = "Тестовое сообщение"

send_email(smtp_server, smtp_port, sender, recipient, fake_from, subject, body)