import smtplib

from email.message import EmailMessage
from email.headerregistry import Address


def sendemail(from_addr: str, to_addr: str, subject: str, message: str, login: str, password: str,
              smtpserver: str):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = Address("Apartment Alert", from_addr)
    msg["To"] = Address("Applicant", to_addr)
    msg.set_content(message)

    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    server.sendmail(from_addr, to_addr, str(msg))
    server.quit()
