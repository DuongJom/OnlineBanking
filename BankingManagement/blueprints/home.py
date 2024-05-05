from flask import Blueprint, render_template, session
from bson import ObjectId

from models import database
from helpers import login_required

db = database.Database().get_db()
accounts = db['accounts']

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
@login_required
def index():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    return render_template('home.html', account = account)


