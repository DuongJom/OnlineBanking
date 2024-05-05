import random
from flask import redirect, session
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from app import app, mail
from SysEnum import MIMEType

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("account_id") is None:
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

def send_email(recipients, subject, html, cc=None, bcc=None, attachments = None):
    msg = Message()
    msg.sender = (app.config['MAIL_DEFAULT_SENDER'], app.config['MAIL_USERNAME'])
    msg.subject = subject
    msg.html = html

    # check if we need to sen to multiple recipients
    if type(recipients) is list and len(recipients) > 0:
        msg.recipients = recipients
    else:
        msg.recipients=[recipients]

    # check to send to cc
    if type(cc) is list and len(cc) > 0:
        msg.cc = cc

    # check to send to bcc
    if type(bcc) is list and len(bcc) > 0:
        msg.bcc = bcc

    if type(attachments) is list and len(attachments) > 0:
        for attachment in attachments:
            with open(attachment['path'], 'rb') as attached_file:
                msg.attach(attachment['filename'], attachment['mime_type'], attached_file.read())

    mail.send(msg)

def getMIMETypeValue(mime_type: MIMEType):
    prefix = 'application/'

    if mime_type == MIMEType.HTML:
        return 'text/html'
    
    if mime_type == MIMEType.TEXT:
        return 'text/plain'
    
    if mime_type == MIMEType.IMG_PNG:
        return 'image/png'
    
    if mime_type == MIMEType.IMG_JPG:
        return 'image/jpeg'
    
    if mime_type == MIMEType.IMG_BMP:
        return 'image/bmp'
    
    if mime_type == MIMEType.PDF:
        return prefix + 'pdf'
    
    if mime_type == MIMEType.XML:
        return prefix + 'xml'
    
    if mime_type == MIMEType.EXCEL_XLS:
        return prefix + 'vnd.ms-excel'
    
    if mime_type == MIMEType.EXCEL_XLSX:
        return prefix + 'vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    
    if mime_type == MIMEType.EXCEL_XLSM:
        return prefix + 'vnd.ms-excel.sheet.macroEnabled.12'
    
    if mime_type == MIMEType.WORD_DOC or mime_type == MIMEType.WORD_DOT:
        return prefix + 'msword'
    
    if mime_type == MIMEType.WORD_DOCX:
        return prefix + 'vnd.openxmlformats-officedocument.wordprocessingml.document'
    
    if mime_type == MIMEType.WORD_DOTX:
        return prefix + 'vnd.openxmlformats-officedocument.wordprocessingml.template'
    
    if mime_type == MIMEType.AUDIO:
        return 'audio/mp4;audio/mpeg;application/ogg'
    
    if mime_type == MIMEType.VIDEO:
        return 'video/mpeg'
    
    
    
