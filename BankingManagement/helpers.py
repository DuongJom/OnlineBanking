import random
import os
from flask import redirect, session, render_template
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import app, mail

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("userId") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def issueNewCard():
    cardNum = str(random.randint(10**13,(10**14)-1))
    accountNum = str(random.randint(10**13,(10**14)-1))
    cvvNum = str(random.randint(100,999))
    return {
        'cardNumber':cardNum, 
        'cvvNumber': cvvNum,
        'accountNumber': accountNum
    }

ts = URLSafeTimedSerializer(app.secret_key)
def get_token(user_email, salt):
    # dumps convert python object to JSON string
      token = ts.dumps(user_email, salt)
      return token

def send_email(recipient, subject, html):
    msg = Message()
    msg.sender = ("no-reply@gmail.com", app.config['MAIL_USERNAME'])
    msg.subject = subject
    msg.recipients = [recipient]
    msg.html = html
    mail.send(msg)
