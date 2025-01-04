import time
import random
from flask import Blueprint, render_template, session, redirect, request, flash
from bson import ObjectId
from datetime import datetime as dt

from models import database, transaction, investment as investmnt
from message import messages_success, messages_failure
from helpers.helpers import login_required, get_banks, generate_otp, send_email
from enums.transaction_type import TransactionType
from enums.bill_status import BillStatusType
from enums.investment import InvestmentType
from enums.currency import CurrencyType

db = database.Database().get_db()
accounts = db['accounts']
transactions = db['transactions']
users = db['users']
bills = db['bills']
investments = db['investments']

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/", methods=["GET"])
@login_required
def home():
    account_id = ObjectId(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    if account:
        query = {
            "$or": [
                {"SenderId": account['AccountNumber']},
                {"ReceiverId": account['AccountNumber']}
            ]
        }
        transactions_data = transactions.find(query)
        transactions_of_account = [
            {
                "date": transaction["TransactionDate"], 
                "description": transaction["Message"], 
                "amount": transaction["Amount"], 
                "balance": transaction["CurrentBalance"], 
                "info": transaction
            }
            for transaction in transactions_data
        ]

        return render_template('/user/dashboard.html', 
                            account=account,
                            transactions_list=transactions_of_account)
    
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
            amount = float(amount),
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
@login_required
def bill_payment():
    if request.method == "GET":
        today = dt.today()
        start_date = dt(today.year, today.month, 1)
        query = {
            "$and": [
                { "Status": BillStatusType.UNPAID.value},
                { "InvoiceDate": { "$gte": start_date}},
                { "InvoiceDate": { "$lte": today}}
            ]
        }

        lst_bills = list(bills.find(query))
        return render_template(
            "/user/bill_payment.html",
            bills=lst_bills,
            start_date=start_date.date(),
            end_date=today.date())
    
    start_date = request.form['start_date']
    end_date = request.form['end_date']

    if start_date:
        start_date = dt.strptime(start_date, "%Y-%m-%d")
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

    if end_date:
        end_date = dt.strptime(end_date, "%Y-%m-%d")
        # Set the time to 23:59:59 to include the full end date
        end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

    query = {"Status": BillStatusType.UNPAID.value}
    if start_date and end_date:
        query = {
            "$and": [
                { "Status": BillStatusType.UNPAID.value},
                { "InvoiceDate": { "$gte": start_date}},
                { "InvoiceDate": { "$lte": end_date}}
            ]
        }
    elif start_date and not end_date:
        query = {
            "$and": [
                { "Status": BillStatusType.UNPAID.value},
                { "InvoiceDate": { "$gte": start_date}}
            ]
        }
    elif not start_date and end_date:
        query = {
            "$and": [
                { "Status": BillStatusType.UNPAID.value},
                { "InvoiceDate": { "$lte": end_date}}
            ]
        }

    lst_bills = list(bills.find(query))
    return render_template(
            "/user/bill_payment.html",
            bills=lst_bills,
            start_date=start_date.date(),
            end_date=end_date.date())

@user_blueprint.route('/payment', methods=['POST'])
@login_required
def payment():
    try:
        account_id = ObjectId(session.get("account_id"))
        bill_id = request.form.get('bill')
        payment_method = request.form.get('payment_method')
        amount = request.form.get('amount')

        if bill_id != -1:
            bill = bills.find_one({"_id": ObjectId(bill_id)})
            account_number = request.form.get('account_number')
            if bill:
                find_query = {
                    "$and":[
                        {"_id": ObjectId(account_id)},
                        {"AccountNumber": account_number}
                    ]
                }
                account = accounts.find_one(find_query)

                if not account:
                    flash(messages_failure['account_not_found'], 'error')
                    return redirect(request.referrer)
                
                if account["Balance"] < float(amount):
                    flash(messages_failure['balance_not_enough'].format('pay the bill'), 'error')
                    return redirect(request.referrer)
                
                bills.update_one(
                    {"_id": ObjectId(bill_id)},
                    {
                        "$set": {
                            "Status": BillStatusType.PAID.value,
                            "PaymentMethod": payment_method
                        }
                    }
                )

                accounts.update_one(
                    {"_id": ObjectId(account_id)},
                    {
                        "$set": {
                            "Balance": account["Balance"] - float(amount),
                        }
                    }
                )

                trans = transaction.Transaction(
                    sender = account['AccountNumber'],
                    receiver = bill_id,
                    amount = float(amount),
                    currency = account['Currency'],
                    message = f"Payment for {bill['BillType']} bill of {bill['InvoiceDate'].strftime('%Y/%m/%d')}",
                    transaction_type = TransactionType.PAYMENT.value,
                    balance = account['Balance'] - float(amount)
                )
                transactions.insert_one(trans.to_json())
                flash(messages_success['payment_bill_success'], 'success')
    except Exception as e:
        print(e)
        flash(messages_failure['internal_server_error'], "error")
        return redirect(request.referrer)
    return redirect('/bill-payment')

@user_blueprint.route('/investment-savings',methods=['GET'])
@login_required
def investment_savings():
    if request.method == "GET":
        account_id = ObjectId(session.get("account_id"))
        currency = None
        if account_id:
            account = accounts.find_one({'_id':ObjectId(account_id)})
            currency_value = account['Currency']
            if currency_value == CurrencyType.VND.value:
                currency = CurrencyType.VND.name
            elif currency_value == CurrencyType.USD.value:
                currency = CurrencyType.USD.name
            else:
                currency = CurrencyType.EUR.name
        else:
            currency = 'USD'
        
        today = dt.today()
        lst_investments = list(investments.find({}))
        
        for investment in lst_investments:
            lasted_update = dt.strptime(investment['ModifiedDate'],'%Y-%m-%dT%H:%M:%S.%f').date()
            if lasted_update != today.date():
                current_investment_rate = round(random.uniform(-10,10),2)
                investments.update_one(
                    {"_id": investment["_id"]},
                    {
                        "$set": {
                            "CurrentRate": current_investment_rate,
                            "CurrentAmount": investment['CurrentAmount'] + investment['CurrentAmount']*(current_investment_rate)/100
                        }
                    }
                )

        return render_template(
            "/user/investment_savings.html", 
            investment_date=today.date(),
            investments=lst_investments,
            currency=currency
        )

@user_blueprint.route('/add-investment-savings',methods=['POST'])
@login_required
def add_new_investment():
    try:
        account_id = ObjectId(session.get("account_id"))
        if account_id:
            account = accounts.find_one({'_id':ObjectId(account_id)})
            if not account:
                flash(messages_failure['account_not_found'], 'error')
                return redirect(request.referrer)
            
            owner = account['AccountOwner']
            investment_name = request.form.get('investment_name')
            investment_type = request.form.get('investment_type')
            investment_amount = request.form.get('investment_amount')
            investment_date = request.form.get('investment_date')
            investment_rate = float(request.form.get('rate')) if request.form.get('rate') else 0

            if not investment_name or not investment_type or int(investment_type) < InvestmentType.STOCK.value or \
                not investment_amount or not investment_date:
                flash(messages_failure['must_input_value'], 'error')
                return redirect(request.referrer)
            
            if account["Balance"] < float(investment_amount):
                flash(messages_failure['balance_not_enough'].format('investment/savings'), 'error')
                return redirect(request.referrer)
            
            type_name = None
            if int(investment_type) == InvestmentType.STOCK.value:
                type_name = "Stock"
            elif int(investment_type) == InvestmentType.BONDS.value:
                type_name = "Bonds"
            elif int(investment_type) == InvestmentType.REAL_ESTATE.value:
                type_name = "Real Estate"
            else:
                type_name = "Crypto"

            investment_date = dt.strptime(investment_date, '%Y-%m-%d')
            investment_date = investment_date.replace(hour=0, minute=0, second=0, microsecond=0)

            investment = investmnt.Investment(
                owner=owner,
                name=investment_name,
                type=type_name,
                investment_amount=investment_amount,
                investment_date= investment_date.isoformat(),
                rate=investment_rate,
                current_amount= float(investment_amount) + float(investment_amount)*investment_rate/100,
                createdBy=owner,
                modifiedBy=owner
            )
            result = investments.insert_one(investment.to_json())
            investment = investments.find_one({'_id': result.inserted_id})

            accounts.update_one(
                {"_id": ObjectId(account_id)},
                {
                    "$set": {
                        "Balance": account["Balance"] - float(investment_amount),
                    }
                }
            )

            trans = transaction.Transaction(
                sender = account['AccountNumber'],
                receiver = result.inserted_id,
                amount = float(investment_amount),
                currency = account['Currency'],
                message = f"Investment for {investment['Name']} of {dt.strptime(investment['InvestmentDate'],'%Y-%m-%dT%H:%M:%S').strftime('%Y/%m/%d')}",
                transaction_type = TransactionType.INVESTMENT.value,
                balance = account['Balance'] - float(investment_amount)
            )
            transactions.insert_one(trans.to_json())
            flash(messages_success['investment_savings_created_success'], 'success')
    except Exception as e:
        print(e)
        flash(messages_failure['internal_server_error'], "error")
        return redirect(request.referrer)
    return redirect('/investment-savings')

@user_blueprint.route('/card-management',methods=['GET', 'POST'])
@login_required
def card_management():
    if request.method == 'GET':
        lst_investment = investments.find({})
        return render_template("/user/card_management.html", investments=lst_investment)

@user_blueprint.route('/loan-management',methods=['GET', 'POST'])
@login_required
def loan_management():
    if request.method == 'GET':
        return render_template('/user/loan_management.html')

@user_blueprint.route('/settings-security',methods=['GET', 'POST'])
@login_required
def settings_security():
    if request.method == 'GET':
        return render_template('/user/settings_security.html')