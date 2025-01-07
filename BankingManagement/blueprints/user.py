from flask import Blueprint, render_template, session, redirect, request, flash
from bson import ObjectId
import time

from models import database, transaction
from message import messages_success, messages_failure
from helpers.helpers import login_required, get_banks, generate_otp, send_email
from enums.transaction_type import TransactionType
from enums.role_type import RoleType

db = database.Database().get_db()
accounts = db['accounts']
transactions = db['transactions']
users = db['users']

user_blueprint = Blueprint('huserome', __name__)

@user_blueprint.route("/money-transfer", methods=["GET", "POST"])
@login_required
def transfer_money():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    banks = get_banks()

    if request.method == "POST":
        # Collect form data
        receiver_account = request.form['receiver_account']
        receiver_bank = request.form['receiver_bank']
        amount = request.form['amount']
        currency = request.form['currency']
        message = request.form['message']

        # Store form data in session before redirecting to OTP confirmation
        session['transfer_data'] = {
            'receiver_account': receiver_account,
            'receiver_bank': receiver_bank,
            'amount': amount,
            'currency': currency,
            'message': message
        }

        # Redirect to OTP confirmation
        return redirect("/confirm-otp")

    return render_template("/user/transfer.html", account=account, banks=banks)

@user_blueprint.route("/", methods=["GET"])
@login_required
def home():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})

    if account["Role"] == RoleType.ADMIN.value:
        return redirect("/admin/account")
    elif account["Role"] == RoleType.EMPLOYEE.value:
        return redirect("/employee/home")
    
    if account:
        query = {
            "$or": [
                {"SenderId": account['AccountNumber']},
                {"ReceiverId": account['AccountNumber']}
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

@user_blueprint.route('/confirm-otp', methods=["GET", "POST"])
@login_required
def confirm_otp():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})

    if request.method == 'GET':
        try:
            if account:
                otp = generate_otp()  # Generate the OTP
                session['otp'] = otp  # Store the OTP in the session
                session['otp_expiration'] = time.time() + 60  # Store OTP expiration time

                # Send OTP email
                html = render_template(
                    '/email/verify_otp.html',
                    otp_code=otp,
                    otp_expiration_time=60,
                    customer_name=account['AccountOwner']['Name']
                )
                send_email(
                    recipients=account['AccountOwner']['Email'],
                    subject="OTP For Money Transfer",
                    html=html
                )
                flash(messages_success['send_otp_success'].format(account['AccountOwner']['Email']), 'success')
                return render_template("/user/otp_confirmation.html")
        
        except Exception as e:
            print(e)  # Log the error
            flash(messages_failure['send_otp_failure'], 'error')
            return redirect('/money-transfer')

    otp_code = ''.join([request.form.get(f'otp{i}') for i in range(1, 7)])  # Concatenate the OTP inputs
    stored_otp = session.get('otp')  # Get the stored OTP
    expiration_time = session.get('otp_expiration')

    # Validate OTP
    if time.time() > expiration_time:
        flash("OTP has expired. Please request a new one.", 'error')
        return redirect(request.path)

    if otp_code == stored_otp:
        # Retrieve transfer data from session
        transfer_data = session.get('transfer_data', {})
        receiver_account = transfer_data.get('receiver_account')
        receiver_bank = transfer_data.get('receiver_bank')
        amount = transfer_data.get('amount')
        currency = transfer_data.get('currency')
        message = transfer_data.get('message')

        accounts.update_one(
            {"AccountNumber": account["AccountNumber"]},
            {
                "$set": {
                    "Balance": account['Balance'] - float(amount)
                }
            }
        )

        trans = transaction.Transaction(
            sender = account['AccountNumber'],
            receiver = receiver_account,
            amount = float(amount)*(-1),
            currency = currency,
            message = message,
            transaction_type = TransactionType.TRANSFER.value,
            balance = account['Balance'] - float(amount)
        )
        transactions.insert_one(trans.to_json())
        flash(messages_success['transfer_money_success'], 'success')
        return redirect("/money-transfer")
    else:
        flash(messages_failure['OTP_invalid'], 'error')
        return redirect(request.path)

@user_blueprint.route('/bill-payment',methods=['GET', 'POST'])
def bill_payment():
    pass

@user_blueprint.route('/top-up',methods=['GET', 'POST'])
def top_up():
    pass

@user_blueprint.route('/card-management',methods=['GET', 'POST'])
def card_management():
    pass

@user_blueprint.route('/investment-savings',methods=['GET', 'POST'])
def investment_savings():
    pass

@user_blueprint.route('/loan-management',methods=['GET', 'POST'])
def loan_management():
    pass

@user_blueprint.route('/settings-security',methods=['GET', 'POST'])
def settings_security():
    pass

@user_blueprint.route('/other-services',methods=['GET', 'POST'])
def other_services():
    pass