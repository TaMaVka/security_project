import smtpd
import asyncore
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import policy
from email.parser import BytesParser

class CustomSMTPServer(smtpd.SMTPServer):
    def process_message(self, peer, mailfrom, rcpttos, data, **my_kwargs):

        try:
            msg = BytesParser(policy=policy.default).parsebytes(data)
            
            print(f"Сообщение от: {mailfrom}")
            print(f"Сообщение для: {', '.join(rcpttos)}")
       
            print(f"Тема: {msg['Subject']}")
            print(f"Отправитель: {msg['From']}")
            print(f"Получатель: {msg['To']}")
            
            if msg.is_multipart():
                for part in msg.iter_parts():
                    if part.get_content_type() == 'text/plain': 
                        body = part.get_content()
                        print(f"Тело письма:\n{body}")
            else:
                body = msg.get_content()
                print(f"Тело письма:\n{body}")
                
        except Exception as e:
            print(f"Ошибка обработки сообщения: {e}")
        
        print("=" * 50)
        return

server = CustomSMTPServer(('127.0.0.1', 1025), None)
print("SMTP-сервер запущен на 127.0.0.1:1025")
try:
    asyncore.loop()
except KeyboardInterrupt:
    print("SMTP-сервер остановлен.")
