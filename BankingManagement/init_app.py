import os

from flask import Flask
from dotenv import load_dotenv

def init(app: Flask):
    # to access configuration variables from root_file/config.py
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    app.salt = os.getenv('SALT')
    app.username_usr01 = os.getenv('USERNAME_USER01')
    app.password_usr01 = os.getenv('PASSWORD_USER01')
    app.username_emp01 = os.getenv('USERNAME_EMPLOYEE01')
    app.password_emp01 = os.getenv('PASSWORD_EMPLOYEE01')
    app.username_adm01 = os.getenv('USERNAME_ADMIN01')
    app.password_adm01 = os.getenv('PASSWORD_ADMIN01')
    app.config.from_object('config')
    
    return app