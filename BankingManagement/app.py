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

from blueprints import account, admin, employee, home

app.register_blueprint(account.account_blueprint)
app.register_blueprint(home.home_blueprint)
app.register_blueprint(employee.employee_blueprint)
app.register_blueprint(admin.admin_blueprint)

if __name__ == '__main__':
    app.run(debug=True)