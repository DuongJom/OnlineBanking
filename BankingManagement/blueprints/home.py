from flask import Blueprint, render_template, session, redirect, request, flash
from bson import ObjectId

from models import database
from message import messages_success, messages_failure
from helpers import login_required, get_banks, generate_otp, send_email

db = database.Database().get_db()
accounts = db['accounts']
transactions = db['transactions']

home_blueprint = Blueprint('home', __name__)

@home_blueprint.route("/money-transfer", methods=["GET", "POST"])
@login_required
def transfer_money():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    banks = get_banks()

    if request.method == "GET":
        return render_template("/user/transfer.html", account=account, banks=banks)

@home_blueprint.route("/", methods=["GET"])
@login_required
def home():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    if account:
        query = {
            "$or": [
                {"SenderId": account_id},
                {"ReceiverId": account_id}
            ]
        }
        transactions_data = transactions.find(query)
        transactions_of_account = [
            {"date": transaction["TransactionDate"], "description": transaction["Message"], "amount": transaction["Amount"], "balance": transaction["CurrentBalance"]}
            for transaction in transactions_data
        ]

        return render_template('/user/dashboard.html', 
                            account=account,
                            transactions_list=transactions_of_account)

@home_blueprint.route('/confirm-otp', methods=['GET','POST'])
@login_required
def confirm_otp():
    if request.method == 'GET':
        try:
            account_id = ObjectId(session.get("account_id"))
            account = accounts.find_one({"_id": account_id})
            if account:
                otp = generate_otp()
                html = render_template('/email/verify_otp.html', otp_code=otp, otp_expiration_time=60, customer_name=account['AccountOwner']['Name'])
                send_email(recipients=account['AccountOwner']['Email'], subject="OTP For Money Transfer", html=html)
                flash(messages_success['send_otp_success'].format(account['AccountOwner']['Email']), 'success')
                return render_template("/user/otp_confirmation.html")
        except:
            flash(messages_failure['send_otp_failure'], 'error')
            return redirect('/money-transfer')
    return redirect("/home")

@home_blueprint.route('/resend-otp', methods=['GET'])
@login_required
def resend_otp():
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