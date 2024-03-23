from flask import Flask
from controllers import account_controller, home_controller
from flask_mail import Mail, Message

app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')
app.config.from_pyfile('config.py')

mail = Mail(app)

app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(home_controller.home_blueprint)

if __name__ == '__main__':
    app.run(debug=True)