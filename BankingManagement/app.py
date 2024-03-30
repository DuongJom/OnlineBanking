from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__, instance_relative_config=True)

# to access configuration variables from root_file/config.py
app.config.from_object('config')

# to access configuration variables from root_file/intances/config.py
app.config.from_pyfile('config.py')

# initialize mail instance
mail = Mail(app)
# initialize csrf protect
csrf = CSRFProtect(app)

from controllers import account_controller, home_controller
app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(home_controller.home_blueprint)

if __name__ == '__main__':
    app.run(debug=True)