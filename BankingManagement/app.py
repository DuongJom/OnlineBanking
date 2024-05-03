from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from init_app import init

app = Flask(__name__)
app = init(app)

# initialize mail instance
mail = Mail(app)
# initialize csrf protect
csrf = CSRFProtect(app)

from controllers import home_controller, account_controller, employee_controller, admin_controller

app.register_blueprint(account_controller.account_blueprint)
app.register_blueprint(home_controller.home_blueprint)
app.register_blueprint(employee_controller.employee_blueprint)
app.register_blueprint(admin_controller.admin_blueprint)

if __name__ == '__main__':
    app.run(debug=True)