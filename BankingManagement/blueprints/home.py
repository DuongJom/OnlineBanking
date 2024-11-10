from flask import Blueprint, render_template, session, redirect, request
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
    if account and account["Role"]:
        if account["Role"]["Value"] == RoleType.USER.value:
            return render_template("/user/home.html", account = account)
        elif account["Role"]["Value"] == RoleType.EMPLOYEE.value:
            return redirect("/employee/home")
        else:
            return redirect("/admin/account")
    return redirect("/login")

@home_blueprint.route("/transfer-money", methods=["GET", "POST"])
@login_required
def transfer_money():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    banks = []
    if request.method == "GET":
        return render_template("/user/transfer.html", account=account, banks=banks)

@home_blueprint.route("/home", methods=["GET"])
def home():
    # Simulate user and transaction data
    user_name = "John Doe"
    account_balance = 1500.00
    account_number = "1234567890"
    transactions = [
        {"date": "2024-11-08", "description": "Grocery Store", "amount": -50.00, "balance": 1450.00},
        {"date": "2024-11-07", "description": "Salary Deposit", "amount": 2000.00, "balance": 1500.00},
        {"date": "2024-11-05", "description": "Utility Bill", "amount": -150.00, "balance": 1350.00},
    ]

    return render_template('/user/dashboard.html', 
                           user_name=user_name, 
                           account_balance=account_balance, 
                           account_number=account_number, 
                           transactions=transactions)