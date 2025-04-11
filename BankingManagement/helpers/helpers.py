import os
import random
import requests
import pandas as pd
import ast
from itsdangerous import URLSafeTimedSerializer
from flask_mail import Message
from dotenv import load_dotenv

from enums.mime_type import MIMEType
load_dotenv()

def issue_new_card():
    cardNum = str(random.randint(10**13,(10**14)-1))
    accountNum = str(random.randint(10**13,(10**14)-1))
    cvvNum = str(random.randint(100,999))
    return {
        'cardNumber':cardNum, 
        'cvvNumber': cvvNum,
        'accountNumber': accountNum
    }

def get_token(app, user_email, salt):
      ts = URLSafeTimedSerializer(app.secret_key)
    # dumps convert python object to JSON string
      token = ts.dumps(user_email, salt)
      return token

def send_email(app, mail, recipients, subject, html, cc=None, bcc=None, attachments = None):
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

def get_banks():
    try:
        headers = {
            'Authorization': f'Bearer {os.getenv("VIETQR_API_KEY")}',
            'Content-Type': 'application/json'
        }
        response = requests.get(os.getenv("VIETQR_API_GET_BANKS_URL"), headers=headers)
        response.raise_for_status()  # Kiểm tra lỗi HTTP
        # Parse kết quả trả về từ VietQR API
        banks_data = response.json()

        # Giả sử dữ liệu trả về có dạng {'banks': [list of banks]}
        banks = banks_data.get('data', [])
        return banks
    except:
        pass

# Function to generate a random OTP
def generate_otp():
    return str(random.randint(100000, 999999))

def get_max_id(database, collection_name):
    lst_collection_name = list(database.list_collection_names())

    if not collection_name in lst_collection_name:
        return 1
    
    collection = database[collection_name]
    lst_data = list(collection.find({}))

    if len(lst_data) < 1:
        return 1
    
    # Sort the list of documents by the '_id' field
    lst_data.sort(key=lambda x: int(x['_id']))

    for i in range(1, len(lst_data)):
        if int(lst_data[i]['_id']) - 1 != int(lst_data[i-1]['_id']):
            return int(lst_data[i-1]['_id']) + 1
    
    return int(lst_data[-1]['_id']) + 1

def get_file_extension(file_name):
    return file_name.split('.')[1] if len(file_name.split('.')) > 0 else None

def flatten_nested_columns(df, nested_columns):
    """
    Flattens nested columns in a DataFrame.
    
    Parameters:
    df (pd.DataFrame): The input DataFrame with potential nested columns.
    nested_columns (list): List of column names that contain nested data (e.g., stringified dictionaries).
    
    Returns:
    pd.DataFrame: The DataFrame with flattened nested columns.
    """
    for col in nested_columns:
        def parse_column(value):
            if isinstance(value, (dict, list)):
                return value
            try:
                return ast.literal_eval(value)
            except (ValueError, SyntaxError):
                return value

        df[col] = df[col].apply(parse_column)
        nested_df = pd.json_normalize(df[col])
        nested_df = nested_df.add_prefix(f'{col}.')
        df = df.drop(columns=[col])
        df = pd.concat([df, nested_df], axis=1)
    
    return df