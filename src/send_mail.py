import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
from threading import Thread

from src.credentials import (login, password)


class EmailThread(Thread):
    def __init__(self, source):
        self.source = source
        super().__init__()

    def run(self):
        msg = MIMEMultipart()
        msg['From'] = login
        msg['To'] = login
        msg['Subject'] = 'New objects detected in the garden!'
        body = 'Attached new images'
        msg.attach(MIMEText(body, 'plain'))

        attachment = open(self.source, 'rb')
        part = MIMEBase('application', "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; "
                                               "filename=" + 'screenshot')
        msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(login, password)
        server.send_message(msg)
