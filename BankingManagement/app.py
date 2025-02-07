from flask import Flask
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from datetime import datetime as dt
from init_app import init
from init_data import initialize_data

app = Flask(__name__)
app = init(app)

# initialize mail instance
mail = Mail(app)
# initialize csrf protect
csrf = CSRFProtect(app)

from blueprints import account, admin, employee, user

app.register_blueprint(account.account_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(employee.employee_blueprint)
app.register_blueprint(admin.admin_blueprint)
initialize_data(app)

@app.template_filter()
def currency_format(value):
    if value is None:
        value = 0
    return "{:,.2f}".format(float(value))

@app.template_filter()
def datetime_format(value, format='%Y-%m-%d %H:%M:%S'):
    if isinstance(value, dt):
        return value.strftime(format)
    value = dt.strptime(value, '%Y-%m-%dT%H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
    return value

@app.template_filter()
def date_format(value):
    return dt.fromisoformat(value).date()

@app.template_filter()
def strip(value):
    return str(value).strip()

if __name__ == '__main__':
    app.run(debug=True)