import os

from flask import Flask
from dotenv import load_dotenv

def init(app: Flask):
    # to access configuration variables from root_file/config.py
    load_dotenv()
    app.secret_key = os.getenv('SECRET_KEY')
    app.salt = os.getenv('SALT')
    app.config.from_object('config')
    
    return app