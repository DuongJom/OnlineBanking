from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import app
from app import mail

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

def send_email(recipient, subject, html):
    msg=Message()
    msg.recipients=[recipient]
    msg.subject=subject
    msg.html=html
    mail.send(msg)