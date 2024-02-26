from flask import Flask
from controllers import account_controller, home_controller

app = Flask(__name__)

app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(home_controller.home_blueprint)

if __name__ == '__main__':
    app.run(debug=True)