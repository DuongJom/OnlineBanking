import random
import hashlib

from flask import redirect, session
from functools import wraps
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from models import database, user as u, address, card, account as acc

from message import messages_success, messages_failure
from app import app, mail
from enums.mime_type import MIMEType
from enums.sex_type import SexType
from enums.role_type import RoleType
from enums.card_type import CardType

db = database.Database().get_db()
accounts = db['accounts']
users = db['users']
card_types = db['card_types']
branches = db['branches']
roles = db['roles']
addresses = db['addresses']
cards = db['cards']


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
    
    
def paginator(page, items_list):
    per_page = 10
    start = (page - 1) * per_page
    end = start + per_page

    render_items = items_list[start:end]

    total_pages = (len(items_list) + per_page - 1) / per_page

    return {'render_items' : render_items, 'total_pages' : total_pages}

def generate_login_info(email, phone):       
    suffix = 0
    username = email.split('@')[0]

    while(accounts.find_one({"Username": username} != None)):
        if suffix != 0:
            username = username.rpartition('_')[0]
        username = username + '_' + str(suffix)
        suffix = suffix + 1

    hash_object = hashlib.sha256(phone.encode())
    hash_hex = hash_object.hexdigest()
    password = hash_hex[:10]

    return {
        "Username": username,
        "Password": password
    }

def verify_input_data(row_index, **kwargs):
    for k, v in kwargs.items():
        if  not isinstance(v,str) or v == None:
            return {'status': "fail", 'message': messages_failure["null_data"].format(k), "row_index": row_index}
        
    if accounts.find_one({"Username": kwargs["Username"]}) != None:
        return {'status': "fail", 'message': messages_failure["username_existed"].format(kwargs["Username"]), "row_index": row_index}
    if users.find_one({"Email": kwargs["Email"]}) != None:
        return {'status': "fail", 'message': messages_failure["email_existed"].format(kwargs["Email"]), "row_index": row_index}
    if users.find_one({"Phone": kwargs["Phone"]}) != None:
        return {'status': "fail", 'message': messages_failure["phone_existed"].format(kwargs["Phone"]), "row_index": row_index}
    
    return {'status': "success", 'message': messages_success["create_success"].format(kwargs["Username"]), "row_index": row_index}

# data is a dictionary account data
def create_accounts(data):
    admin_id = session.get("account_id")
    total = len(data)
    counter = 0
    row_index = 1
    response_data = {"total": total, "logs": []}
    res = None

    for accData in data:
        # User info
        username = accData["Username"].strip()
        gender_text = accData["Gender"].strip()
        gender = None
        if gender_text.lower().strip() == "male":
            gender = SexType.MALE
        elif gender_text.lower().strip() == "female":
            gender = SexType.FEMALE
        else:
            gender = SexType.OTHER

        phone = str(accData["Phone"]).strip()
        email = accData["Email"].strip()

        #account info
        name = accData["Name"].strip()
        text_role = accData["Role"]
        branchName = accData["Branch"].strip()
        loginMethods = accData["Login Method"]
        transferMethods = accData["Transfer Method"]
        text_address = accData["Address"]
        new_address = None
        request_branch = None

        card_type = card_types.find_one({"TypeValue": CardType.CREDITS.value}, {"_id":0})
        card_info = issueNewCard()
        new_card = card.Card(cardNumber=card_info['cardNumber'], cvv=card_info['cvvNumber'], type=card_type, createdBy = admin_id)
        loginInfo = generate_login_info(email, phone)            

        roleValue = None

        if text_role.lower().strip() == "user":
            roleValue = RoleType.USER
        elif text_role.lower().strip() == "employee":
            roleValue = RoleType.EMPLOYEE
        elif text_role.lower().strip() == "admin":
            roleValue = RoleType.ADMIN
        else:
            roleValue = RoleType.USER

        role = roles.find_one({"Value": roleValue.value}, {"_id":0})

        try:
            request_branch = branches.find_one({"BranchName": branchName}, {"_id":0})
        except KeyError:
            request_branch = None
        
        try:
            mar = list(map(lambda x: x.strip(), text_address.split(',')))
            new_address = address.Address(street = mar[0], ward = mar[1], district = mar[2], city = mar[3], country = mar[4], createdBy = admin_id).to_json()
        except:
            new_address = None

        res = verify_input_data(row_index , Username = username, Email = email, Phone = phone)

        if res["status"] == "success":
            counter += 1
            new_user = u.User(name = name, sex = gender, address = new_address, phone = phone, email = email, card = new_card.to_json(), createdBy = admin_id)
            new_account = acc.Account(accountNumber = card_info['accountNumber'], branch = request_branch, user = new_user.to_json(),
                                    username = username, password = loginInfo['Password'], role = role,
                                    transferMethod = transferMethods, loginMethod = loginMethods, createdBy = admin_id)
            
            cards.insert_one(new_card.to_json())
            if new_address != None:
                addresses.insert_one(new_address.to_json())
            users.insert_one(new_user.to_json())
            accounts.insert_one(new_account.to_json())

        row_index += 1
        response_data["logs"].append(res)
        response_data.update({"success_create": counter})
    return response_data
            

            
            
        


