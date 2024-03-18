from flask import Flask, session
from dotenv import load_dotenv
import os

from controllers import account_controller, home_controller

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(home_controller.home_blueprint)

if __name__ == '__main__':
    app.run(debug=True)