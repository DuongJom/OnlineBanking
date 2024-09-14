from flask import Blueprint, render_template, session, redirect
from bson import ObjectId

from models import database
from helpers import login_required
from enums.role_type import RoleType

db = database.Database().get_db()
accounts = db['accounts']

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route('/')
@login_required
def index():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    if account:
        if account["Role"] == RoleType.USER.value:
            return render_template("general/home.html", account = account)
        elif account["Role"] == RoleType.EMPLOYEE.value:
            return redirect("/employee/home")
        else:
            return redirect("/admin/account")
    return redirect("/login")


