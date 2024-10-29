import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class Email:
    def __init__(self, sender, recipient, subject, body, files=None):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.files = files if files is not None else []
        self.date = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    def __str__(self):
        return (
            f"From: {self.sender}\n"
            f"To: {self.recipient}\n"
            f"Subject: {self.subject}\n\n"
            f"{self.body}\n"
        )

    def attach_file(self, file_path):
        try:
            with open(file_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {os.path.basename(file_path)}",
                )
                self.files.append(part)
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден: {file_path}")

def create_email():
    sender = input("Введите email отправителя: ")
    recipient = input("Введите email получателя: ")
    subject = input("Введите тему письма: ")
    body = input("Введите текст письма: ")

    files = []
    attach_file = input("Прикрепить файл? (да/нет): ")
    if attach_file.lower() == "да":
        while True:
            file_path = input("Введите путь к файлу (или пустую строку для завершения): ")
            if not file_path:
                break
            files.append(file_path)

    email = Email(sender, recipient, subject, body, files)
    return email

def send_email(email):
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    email_login = os.getenv("EMAIL_LOGIN")
    email_password = os.getenv("EMAIL_PASSWORD")

    if not all([email_login, email_password]):
        raise ValueError("Ошибка: Не найдены логин или пароль в .env файле.")

    msg = MIMEMultipart()
    msg['From'] = email.sender
    msg['To'] = email.recipient
    msg['Subject'] = email.subject
    msg['Date'] = email.date
    msg.attach(MIMEText(email.body, 'plain'))

    for file_path in email.files:
        email.attach_file(file_path)

    for file in email.files:
        msg.attach(file)

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email_login, email_password)
            server.sendmail(email.sender, email.recipient, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    email = create_email()
    send_email(email)
