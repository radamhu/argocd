import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path

html = Template(Path('index.html').read_text())
email = EmailMessage()
email['from'] = 'Adam Roland'
email['to'] = 'roland.adam@hotmail.com'
email['subject'] = 'Gyere le a kenyerert'

email.set_content(html.substitute({'name': 'Roli'}), 'html')

with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login('csaba.roland.adam@gmail.com', 'uncipanci2000')
    smtp.send_message(email)
    print('postas elvitte a levelet')
