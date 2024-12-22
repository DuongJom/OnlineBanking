from flask import Blueprint, render_template, session, redirect, request
from bson import ObjectId

from models import database
from helpers import login_required
from enums.role_type import RoleType

db = database.Database().get_db()
accounts = db['accounts']

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route("/money-transfer", methods=["GET", "POST"])
@login_required
def transfer_money():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    banks = []
    if request.method == "GET":
        return render_template("/user/transfer.html", account=account, banks=banks)

@home_blueprint.route("/", methods=["GET"])
@login_required
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

@home_blueprint.route('/confirm-otp', methods=['GET','POST'])
@login_required
def confirm_otp():
    #generate OTP code
    if request.method == 'GET':
        return render_template("/user/otp_confirmation.html")
    return redirect("/home")

@home_blueprint.route('/resend-otp',methods=['POST'])
def resend_otp():
    pass

@home_blueprint.route('/account-management',methods=['GET', 'POST'])
def account_management():
    pass

@home_blueprint.route('/bill-payment',methods=['GET', 'POST'])
def bill_payment():
    pass

@home_blueprint.route('/top-up',methods=['GET', 'POST'])
def top_up():
    pass

@home_blueprint.route('/card-management',methods=['GET', 'POST'])
def card_management():
    pass

@home_blueprint.route('/investment-savings',methods=['GET', 'POST'])
def investment_savings():
    pass

@home_blueprint.route('/loan-management',methods=['GET', 'POST'])
def loan_management():
    pass

@home_blueprint.route('/settings-security',methods=['GET', 'POST'])
def settings_security():
    pass

@home_blueprint.route('/other-services',methods=['GET', 'POST'])
def other_services():
    pass