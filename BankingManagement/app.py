from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv
import os


app = Flask(__name__, instance_relative_config=True)
# to access configuration variables from root_file/config.py
load_dotenv()
app.secret_key = os.getenv('SECRET_KEY')
app.config.from_object('config')

# initialize mail instance
mail = Mail(app)
# initialize csrf protect
csrf = CSRFProtect(app)

from controllers import home_controller, account_controller



app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(home_controller.home_blueprint)
    

if __name__ == '__main__':
    app.run(debug=True)