import os
import smtplib
import dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import traceback
from dotenv import load_dotenv
from dotenv import dotenv_values

#print("Текущая рабочая директория:", os.getcwd()) #проверка директории, с которой был запущен код

config = dotenv_values("sas.env")  # укажите точный путь, если файл в другой директории; иначе просто название файла
#print(config)


def create_email(from_email, to_email, subject, body, attachment_path=None):
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    
    if attachment_path:
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename= {os.path.basename(attachment_path)}")
            message.attach(part)
        except Exception as e:
            print(f"Ошибка прикрепления файла: {e}")
            traceback.print_exc()
    
    return message

def send_email(recipient_email):
    smtp_server = config.get("SMTP_SERVER")
    smtp_port = config.get("SMTP_PORT")
    username = config.get("SMTP_USERNAME")
    password = config.get("SMTP_PASSWORD")

    # Проверка на наличие значений переменных окружения
    if not smtp_server or not smtp_port or not username or not password:
        print("Ошибка: Не все переменные окружения загружены. Проверьте файл .env.")
        return

    from_email = username
    to_email = recipient_email
    subject = "Тестовое письмо"
    body = "Привет, работяга!"
    
    attach_file = input("Хотите прикрепить файл? (y/n): ").strip().lower()
    attachment_path = None
    if attach_file == "y":
        attachment_path = input("Введите путь к файлу для прикрепления: ").strip()
    
    message = create_email(from_email, to_email, subject, body, attachment_path)

    server = None
    try:
        server = smtplib.SMTP_SSL(smtp_server, int(smtp_port))
        server.login(username, password)
        server.sendmail(from_email, to_email, message.as_string())
        print("Письмо отправлено успешно.")
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        traceback.print_exc()
    finally:
        if server:
            server.quit()

recipient_email = config.get("RECIPIENT")
send_email(recipient_email)
