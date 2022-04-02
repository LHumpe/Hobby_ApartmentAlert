import smtplib

from email.message import EmailMessage
from email.headerregistry import Address
from typing import List


def sendemail(from_addr: str, to_addr: List[str], subject: str, message: str, login: str, password: str,
              smtpserver: str):
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login, password)
    
    for recip_addr in to_addr:
      
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = Address("Apartment Alert", from_addr)
        msg["To"] = Address("Applicant", recip_addr)
        msg.set_content(message)

        server.sendmail(from_addr, recip_addr, str(msg))
        
        del msg
        
    server.quit()
