from flask import Flask, g
from flask_mail import Mail
from flask_wtf.csrf import CSRFProtect
from init_app import init
from init_data import initialize_data
from filters import (
    currency_format, datetime_format, 
    date_format, strip, format_date, 
    format_card_number, format_id, 
    currency_to_text
)
import uuid
from datetime import datetime as dt
from helpers.logger import logger
from helpers.helpers import get_banks
from flask_caching import Cache

app = Flask(__name__)
app = init(app)
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)
cache.set('banks', get_banks())

# initialize mail instance
mail = Mail(app)
# initialize csrf protect
csrf = CSRFProtect(app)

# Request ID middleware
@app.before_request
def before_request():
    g.request_id = str(uuid.uuid4())
    logger.info(f"New request started with ID: {g.request_id}")

from blueprints import account, admin, employee, user

app.register_blueprint(account.account_blueprint)
app.register_blueprint(user.user_blueprint)
app.register_blueprint(employee.employee_blueprint)
app.register_blueprint(admin.admin_blueprint)
initialize_data(app)

# Register the template filters
app.jinja_env.filters['currency_format'] = currency_format
app.jinja_env.filters['datetime_format'] = datetime_format
app.jinja_env.filters['date_format'] = date_format
app.jinja_env.filters['strip'] = strip
app.jinja_env.filters['format_date'] = format_date
app.jinja_env.filters['format_card_number'] = format_card_number
app.jinja_env.filters['format_id'] = format_id
app.jinja_env.filters['currency_to_text'] = currency_to_text
app.jinja_env.globals['now'] = dt.now

if __name__ == '__main__':
    app.run(debug=True)