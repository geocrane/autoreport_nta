import datetime
import smtplib

from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import COMMASPACE

def send_mail(attachments):
    date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    sender = 'geo-rnd@mail.ru'
    receivers = ['ssezhuravlev@sberbank.ru', 'geo-rnd@yandex.ru']
    # 'ssezhuravlev@sberbank.ru',
    subject = f'NTA_stats {date}'
    body = f'NTA_stats {date}'


    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for files in attachments:
        filename = files.split("/")[-1]
        with open(files, 'rb') as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition','attachment', filename=filename)
        msg.attach(part)

    smtp_server = 'smtp.mail.ru'
    smtp_port = 465
    smtp_login = 'geo-rnd@mail.ru'
    smtp_password = 'b4fH8Xt3MDh1Xz0Jz5t9'

    smtp_obj = smtplib.SMTP_SSL(smtp_server, smtp_port)
    smtp_obj.login(smtp_login, smtp_password)
    smtp_obj.sendmail(sender, receivers, msg.as_string())
    smtp_obj.quit()


def send_error(err):
    sender = 'geo-rnd@mail.ru'
    receivers = ['geo-rnd@yandex.ru']
    subject = 'ERROR: statistic_NTA'
    body = f'ERROR: {err}'


    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = COMMASPACE.join(receivers)
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    smtp_server = 'smtp.mail.ru'
    smtp_port = 465
    smtp_login = 'geo-rnd@mail.ru'
    smtp_password = 'b4fH8Xt3MDh1Xz0Jz5t9'

    smtp_obj = smtplib.SMTP_SSL(smtp_server, smtp_port)
    smtp_obj.login(smtp_login, smtp_password)
    smtp_obj.sendmail(sender, receivers, msg.as_string())
    smtp_obj.quit()