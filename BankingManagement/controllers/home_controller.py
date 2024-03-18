from flask import Blueprint, render_template, session
from bson import ObjectId

from helpers import login_required
from controllers.account_controller import collection

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
@login_required
def index():
    userId = ObjectId(session.get("userId"))
    user = collection.find_one({"_id": userId})

    return render_template('home.html', logined_user = user)