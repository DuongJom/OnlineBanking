import time
import random
from flask import Blueprint, render_template, redirect, flash, url_for, session, request
from datetime import datetime as dt

from models import database, transaction, investment as investmnt
from message import messages_success, messages_failure
from helpers.helpers import login_required, get_banks, generate_otp, send_email, get_max_id
from enums.transaction_type import TransactionType
from enums.bill_status import BillStatusType
from enums.investment import InvestmentType
from enums.currency import CurrencyType
from enums.investment_status import InvestmentStatus
from enums.collection import CollectionType
from enums.deleted_type import DeletedType
from enums.role_type import RoleType
from app import app, mail

db = database.Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
transactions = db[CollectionType.TRANSACTIONS.value]
users = db[CollectionType.USERS.value]
bills = db[CollectionType.BILLS.value]
investments = db[CollectionType.INVESTMENTS_SAVINGS.value]
cards = db[CollectionType.CARDS.value]
loans = db[CollectionType.LOANS.value]

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/", methods=["GET"])
@login_required
def home():
    account_id = int(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    if account["Role"] == RoleType.ADMIN.value:
        return redirect(url_for('admin_account.admin_account', page_no=1))
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
            {
                "date": transaction["TransactionDate"], 
                "description": transaction["Message"], 
                "amount": transaction["Amount"], 
                "balance": transaction["CurrentBalance"], 
                "info": transaction
            }
            for transaction in transactions_data
        ]
        
        owner = None
        if account["AccountOwner"]:
            owner = users.find_one({"_id": int(account["AccountOwner"])})

        return render_template('/user/dashboard.html', 
                            account=account,
                            owner=owner,
                            transactions_list=transactions_of_account)
    
@user_blueprint.route("/money-transfer", methods=["GET", "POST"])
@login_required
def transfer_money():
    account_id = int(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    banks = get_banks()
    owner = None
    if account["AccountOwner"]:
        owner = users.find_one({"_id": int(account["AccountOwner"])})

    if request.method == "POST":
        receiver_account = request.form['receiver_account']
        receiver_bank = request.form['receiver_bank']
        amount = request.form['amount']
        currency = request.form['currency']
        message = request.form['message']

        session['transfer_data'] = {
            'receiver_account': receiver_account,
            'receiver_bank': receiver_bank,
            'amount': amount,
            'currency': currency,
            'message': message
        }

        return redirect("/confirm-otp")

    return render_template("/user/transfer.html", account=account, banks=banks, owner=owner)

@user_blueprint.route('/confirm-otp', methods=["GET", "POST"])
@login_required
def confirm_otp():
    account_id = int(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})

    if request.method == 'GET':
        try:
            if account:
                otp = generate_otp()
                session['otp'] = otp
                session['otp_expiration'] = time.time() + 60
                owner = None

                if account["AccountOwner"]:
                    owner = users.find_one({"_id": int(account["AccountOwner"])})
                    
                html = render_template(
                    '/email/verify_otp.html',
                    otp_code=otp,
                    otp_expiration_time=60,
                    customer_name=owner['Name']
                )
                send_email(
                    app=app,
                    mail=mail,
                    recipients=owner['Email'],
                    subject="OTP For Money Transfer",
                    html=html
                )
                flash(messages_success['send_otp_success'].format(owner['Email']), 'success')
                return render_template("/user/otp_confirmation.html")
        
        except Exception as e:
            flash(messages_failure['send_otp_failure'], 'error')
            return redirect('/money-transfer')

    otp_code = ''.join([request.form.get(f'otp{i}') for i in range(1, 7)])
    stored_otp = session.get('otp')
    expiration_time = session.get('otp_expiration')

    if time.time() > expiration_time:
        flash("OTP has expired. Please request a new one.", 'error')
        return redirect(request.path)

    if otp_code == stored_otp:
        transfer_data = session.get('transfer_data', {})
        receiver_account_number = transfer_data.get('receiver_account')
        amount = transfer_data.get('amount')
        currency = transfer_data.get('currency')
        message = transfer_data.get('message')

        accounts.update_one(
            {"AccountNumber": account["AccountNumber"]},
            {
                "$set": {
                    "Balance": account['Balance'] - float(amount),
                    "ModifiedBy": int(account['AccountOwner']),
                    "ModifiedDate": dt.today()
                }
            }
        )

        receiver_account = accounts.find_one({"AccountNumber": receiver_account_number})
        if receiver_account:
            accounts.update_one(
                {"AccountNumber": receiver_account_number},
                {
                    "$set": {
                        "Balance": receiver_account['Balance'] + float(amount),
                        "ModifiedBy": int(account['AccountOwner']),
                        "ModifiedDate": dt.today()
                    }
                }
            )
        transaction_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
        trans = transaction.Transaction(
            id=transaction_id,
            sender = account['AccountNumber'],
            receiver = receiver_account_number,
            amount = float(amount),
            currency = currency,
            message = message,
            transaction_type = TransactionType.TRANSFER.value,
            balance = account['Balance'] - float(amount),
            createdBy = int(account['AccountOwner']),
            modifiedBy = int(account['AccountOwner'])
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
        account_id = int(session.get("account_id"))
        bill_id = request.form.get('bill')
        payment_method = request.form.get('payment_method')
        amount = request.form.get('amount')

        if int(bill_id) != -1:
            bill = bills.find_one({"_id": int(bill_id)})
            account_number = request.form.get('account_number')
            if bill:
                find_query = {
                    "$and":[
                        {"_id": account_id},
                        {"AccountNumber": account_number}
                    ]
                }
                account = accounts.find_one(find_query)

                if not account:
                    flash(messages_failure['account_not_found'], 'error')
                    return redirect(request.referrer)
                
                if float(account["Balance"]) < float(amount):
                    flash(messages_failure['balance_not_enough'].format('pay the bill'), 'error')
                    return redirect(request.referrer)
                
                bills.update_one(
                    {"_id": int(bill_id)},
                    {
                        "$set": {
                            "Status": BillStatusType.PAID.value,
                            "PaymentMethod": payment_method,
                            "ModifiedDate": dt.today(),
                            "ModifiedBy": int(account["AccountOwner"])
                        }
                    }
                )

                accounts.update_one(
                    {"_id": int(account_id)},
                    {
                        "$set": {
                            "Balance": account["Balance"] - float(amount),
                            "ModifiedDate": dt.today(),
                            "ModifiedBy": int(account["AccountOwner"])
                        }
                    }
                )

                transaction_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
                trans = transaction.Transaction(
                    id = transaction_id,
                    sender = account['AccountNumber'],
                    receiver = bill_id,
                    amount = float(amount),
                    currency = account['Currency'],
                    message = f"Payment for {bill['BillType']} bill of {bill['InvoiceDate'].strftime('%Y/%m/%d')}",
                    transaction_type = TransactionType.PAYMENT.value,
                    balance = account['Balance'] - float(amount),
                    createdBy = int(account['AccountOwner']),
                    modifiedBy = int(account['AccountOwner'])
                )
                transactions.insert_one(trans.to_json())
                flash(messages_success['payment_bill_success'], 'success')
    except Exception as e:
        flash(messages_failure['internal_server_error'], "error")
        return redirect(request.referrer)
    return redirect('/bill-payment')

@user_blueprint.route('/investment-savings',methods=['GET'])
@login_required
def investment_savings():
    if request.method == "GET":
        account_id = int(session.get("account_id"))
        account = None
        currency = None
        if account_id:
            account = accounts.find_one({'_id': account_id})
            currency_value = int(account['Currency'])
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
            lasted_update = dt.strptime(str(investment['ModifiedDate']), '%Y-%m-%dT%H:%M:%S.%f').date() if "T" in str(investment['ModifiedDate']) else dt.strptime(str(investment['ModifiedDate']), '%Y-%m-%d %H:%M:%S.%f').date()
            if lasted_update != today.date():
                current_investment_rate = round(random.uniform(-10,10),2)
                investments.update_one(
                    {"_id": investment["_id"]},
                    {
                        "$set": {
                            "CurrentRate": current_investment_rate,
                            "CurrentAmount": investment['CurrentAmount'] + investment['InvestmentAmount']*(current_investment_rate)/100,
                            "ModifiedDate": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                            "ModifiedBy": int(account["AccountOwner"])
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
        account_id = int(session.get("account_id"))
        if account_id:
            account = accounts.find_one({'_id': account_id})
            if not account:
                flash(messages_failure['account_not_found'], 'error')
                return redirect(request.referrer)
            
            owner_id = account['AccountOwner']
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

            investment_id = get_max_id(database=db, collection_name=CollectionType.INVESTMENTS_SAVINGS.value)
            investment = investmnt.Investment(
                id = investment_id,
                owner = int(owner_id),
                name = investment_name,
                type = type_name,
                investment_amount = float(investment_amount),
                investment_date = investment_date.isoformat(),
                rate = investment_rate,
                current_amount = float(investment_amount) + float(investment_amount)*investment_rate/100,
                createdBy = int(owner_id),
                modifiedBy = int(owner_id)
            )

            investments.insert_one(investment.to_json())
            investment = investments.find_one({'_id': investment_id})
            today = dt.today()

            accounts.update_one(
                {"_id": account_id},
                {
                    "$set": {
                        "Balance": account["Balance"] - float(investment_amount),
                        "ModifiedDate": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "ModifiedBy": int(owner_id)
                    }
                }
            )

            transaction_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
            trans = transaction.Transaction(
                id = transaction_id,
                sender = account['AccountNumber'],
                receiver = investment_id,
                amount = float(investment_amount),
                currency = account['Currency'],
                message = f"Investment for {investment['Name']} of {dt.strptime(investment['InvestmentDate'],'%Y-%m-%dT%H:%M:%S').strftime('%Y/%m/%d')}",
                transaction_type = TransactionType.INVESTMENT.value,
                balance = account['Balance'] - float(investment_amount),
                createdBy = int(owner_id),
                modifiedBy = int(owner_id)
            )
            transactions.insert_one(trans.to_json())
            flash(messages_success['investment_savings_created_success'], 'success')
    except Exception as e:
        print(e)
        flash(messages_failure['internal_server_error'], "error")
        return redirect(request.referrer)
    return redirect('/investment-savings')

@user_blueprint.route('/edit-investment', methods=['POST'])
@login_required
def edit_investment():
    try:
        today = dt.today()
        account_id = int(session.get("account_id"))
        account = None

        if account_id:
            account = accounts.find_one({'_id':account_id})
            if not account:
                flash(messages_failure['account_not_found'], 'error')
                return redirect(request.referrer)
        
        investment_id = request.form.get('investment_id')
        edit_type = request.form.get('edit_type')

        if investment_id:
            investment = investments.find_one({'_id': int(investment_id)})
            if not investment:
                flash(messages_failure['investment_not_exist'], 'error')
                return redirect(request.referrer)

            account_balance = 0
            edit_type_name = None
            set_query = {}
            amount = 0
            if int(edit_type) == InvestmentStatus.WITH_DRAW.value:
                set_query = {
                    "$set": {
                        "CurrentAmount": 0,
                        "Status": InvestmentStatus.WITH_DRAW.value,
                        "ModifiedDate": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "ModifiedBy": int(account["AccountOwner"])
                    }
                }
                edit_type_name = "Withdraw"
                amount = investment['CurrentAmount']
            elif int(edit_type) == InvestmentStatus.CANCEL.value:
                set_query = {
                    "$set": {
                        "CurrentAmount": 0,
                        "Status": InvestmentStatus.CANCEL.value,
                        "ModifiedDate": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "ModifiedBy": int(account["AccountOwner"])
                    }
                }
                edit_type_name = "Cancel"
                amount = investment['InvestmentAmount']
            account_balance = account['Balance'] + amount

            accounts.update_one(
                {'_id': account_id},
                {
                    "$set": {
                        "Balance": account_balance,
                        "ModifiedDate": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "ModifiedBy": int(account["AccountOwner"])
                    }
                }
            )

            trans_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
            trans = transaction.Transaction(
                id = trans_id,
                sender = "DHC Bank",
                receiver = account['AccountNumber'],
                amount = amount,
                currency = account['Currency'],
                message = f"{edit_type_name} from {investment['Name']} of {dt.strptime(investment['InvestmentDate'],'%Y-%m-%dT%H:%M:%S').strftime('%Y/%m/%d')}",
                transaction_type = TransactionType.WITHDRAWAL.value,
                balance = account_balance
            )
            transactions.insert_one(trans.to_json())

            investments.update_one(
                {'_id': int(investment_id)},
                set_query
            )
            flash(messages_success['withdraw_cancel_success'].format(edit_type_name), 'success')

    except Exception:
        flash(messages_failure['internal_server_error'], 'error')
    
    return redirect(request.referrer)

@user_blueprint.route('/card-management', methods=['GET', 'POST'])
@login_required
def card_management():
    account_id = int(session.get("account_id"))
    if request.method == "GET":
        account = accounts.find_one({"_id": account_id})
        user = users.find_one({"_id": int(account["AccountOwner"])})
        lst_card = []
        
        for card_id in list(user["Card"]):
            pipeline = [
                {"$match": {"_id": card_id}},
                {
                    "$lookup": {
                        "from": "card_types",
                        "localField": "Type",
                        "foreignField": "_id",
                        "as": "card_info"
                    }
                },
                {
                    "$unwind": "$card_info"
                }
            ]

            result = list(cards.aggregate(pipeline=pipeline))
            if result:
                lst_card.append(result[0])
        
        return render_template("/user/card.html", cards=lst_card, user=user)
    
@user_blueprint.route('/lock-card/<id>', methods=['GET'])
@login_required
def lock_card(id):
    try:
        cards.update_one(
            { "_id": int(id)},
            {
                "$set": {
                    "IsDeleted": DeletedType.DELETED.value,
                    "ModifiedBy": int(session.get("account_id")),
                    "ModifiedDate": dt.now()
                }
            }
        )
        flash(messages_success["locking_card_success"], "success")
    except Exception:
        flash(messages_failure["internal_server_error"], "error")
    finally:
        return redirect(url_for("user.card_management"))
    
@user_blueprint.route('/unlock-card/<id>', methods=['GET'])
@login_required
def unlock_card(id):
    try:
        cards.update_one(
            { "_id": int(id)},
            {
                "$set": {
                    "IsDeleted": DeletedType.AVAILABLE.value,
                    "ModifiedBy": int(session.get("account_id")),
                    "ModifiedDate": dt.now()
                }
            }
        )
        flash(messages_success["unlocking_card_success"], "success")
    except Exception:
        flash(messages_failure["internal_server_error"], "error")
    finally:
        return redirect(url_for("user.card_management"))

@user_blueprint.route('/loan-management',methods=['GET'])
def loan_management():
    account_id = int(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    lst_loan = list(loans.find({"Owner": int(account["AccountOwner"])}))
    return render_template("/user/loan.html", loans=lst_loan)

@user_blueprint.route('/settings-security',methods=['GET', 'POST'])
def settings_security():
    pass

@user_blueprint.route('/other-services',methods=['GET', 'POST'])
def other_services():
    pass