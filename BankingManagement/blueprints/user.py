import time
import random
from flask import Blueprint, render_template, redirect, flash, url_for, session, request
from datetime import datetime as dt

from models import transaction, investment as investment_model
from message import messages_success, messages_failure
from helpers.helpers import get_banks, generate_otp, send_email, get_max_id
from enums.transaction_type import TransactionType
from enums.bill_status import BillStatusType
from enums.investment import InvestmentType
from enums.currency import CurrencyType
from enums.investment_status import InvestmentStatus
from enums.collection import CollectionType
from enums.deleted_type import DeletedType
from enums.role_type import RoleType
from app import app, mail
from decorators import login_required, role_required, log_request
from init_database import (
    db, accounts, users, transactions, bills, investments, loans, cards
)

user_blueprint = Blueprint('user', __name__)

@user_blueprint.route("/", methods=["GET"])
@login_required
@log_request()
@role_required(RoleType.USER.value)
def home():
    account_id = int(session.get("account_id"))
    account_doc = accounts.find_one({"_id": account_id})

    if account_doc:
        query = {
            "$or": [
                {"sender_id": account_doc['account_number']},
                {"receiver_id": account_doc['account_number']}
            ]
        }

        transactions_data = transactions.find(query)
        transactions_of_account = [
            {
                "date": transaction_dt["transaction_date"],
                "description": transaction_dt["message"],
                "amount": transaction_dt["amount"],
                "balance": transaction_dt["current_balance"],
                "info": transaction_dt
            }
            for transaction_dt in transactions_data
        ]
        
        owner = None

        if account_doc["account_owner"]:
            owner = users.find_one({"_id": int(account_doc["account_owner"])})

        return render_template('user/dashboard.html',
                            account=account_doc,
                            owner=owner,
                            transactions_list=transactions_of_account)

    return redirect(url_for("account.login"))
    
@user_blueprint.route("/money-transfer", methods=["GET", "POST"])
@login_required
@log_request()
@role_required(RoleType.USER.value)
def transfer_money():
    account_id = int(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    banks = get_banks()
    owner = None

    if account["account_owner"]:
        owner = users.find_one({"_id": int(account["account_owner"])})

    if request.method == "POST":
        receiver_account = request.form['receiver_account']
        receiver_bank = request.form['receiver_bank']
        amount = request.form['amount']
        currency_value = request.form['currency']
        message = request.form['message']

        session['transfer_data'] = {
            'receiver_account': receiver_account,
            'receiver_bank': receiver_bank,
            'amount': amount,
            'currency': currency_value,
            'message': message
        }

        return redirect("/confirm-otp")

    return render_template("user/transfer.html", account=account, banks=banks, owner=owner)

@user_blueprint.route('/confirm-otp', methods=["GET", "POST"])
@login_required
@log_request()
@role_required(RoleType.USER.value)
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

                if account["account_owner"]:
                    owner = users.find_one({"_id": int(account["account_owner"])})
                    
                html = render_template(
                    'email/verify_otp.html',
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
                return render_template("user/otp_confirmation.html")
        
        except Exception as e:
            print(e)
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
        currency_value = transfer_data.get('currency')
        message = transfer_data.get('message')

        accounts.update_one(
            {"account_number": account["account_number"]},
            {
                "$set": {
                    "balance": account['balance'] - float(amount),
                    "modified_by": int(account['account_owner']),
                    "modified_date": dt.today()
                }
            }
        )

        receiver_account = accounts.find_one({"account_number": receiver_account_number})
        if receiver_account:
            accounts.update_one(
                {"account_number": receiver_account_number},
                {
                    "$set": {
                        "balance": receiver_account['balance'] + float(amount),
                        "modified_by": int(account['account_owner']),
                        "modified_date": dt.today()
                    }
                }
            )
        transaction_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
        trans = transaction.Transaction(
            id=transaction_id,
            sender = account['account_number'],
            receiver = receiver_account_number,
            amount = float(amount),
            currency = currency_value,
            message = message,
            transaction_type = TransactionType.TRANSFER.value,
            balance = account['balance'] - float(amount),
            createdBy = int(account['account_owner']),
            modified_by = int(account['account_owner'])
        )
        transactions.insert_one(trans.to_json())
        flash(messages_success['transfer_money_success'], 'success')
        return redirect("/money-transfer")
    else:
        flash(messages_failure['OTP_invalid'], 'error')
        return redirect(request.path)


@user_blueprint.route('/bill-payment', methods=['GET', 'POST'])
@login_required
@log_request()
@role_required(RoleType.USER.value)
def bill_payment():
    today = dt.today()
    default_start_date = dt(today.year, today.month, 1)
    default_end_date = today
    start_date = default_start_date
    end_date = default_end_date
    status_filter = BillStatusType.UNPAID.value
    query = []

    if request.method == "POST":
        start_date_raw = request.form.get('start_date', '')
        end_date_raw = request.form.get('end_date', '')
        status_filter = request.form.get('status_filter', 'all')

        if start_date_raw:
            start_date = dt.strptime(start_date_raw, "%Y-%m-%d")
            start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)

        if end_date_raw:
            end_date = dt.strptime(end_date_raw, "%Y-%m-%d")
            end_date = end_date.replace(hour=23, minute=59, second=59, microsecond=999999)

        query.append({"account_id": int(session["account_id"])})
        query.append({"invoice_date": {"$gte": start_date}})
        query.append({"invoice_date": {"$lte": end_date}})

        if status_filter in ["0", "1"]:
            query.append({"status": int(status_filter)})

    else:
        query = [
            {"invoice_date": {"$gte": default_start_date}},
            {"invoice_date": {"$lte": default_end_date}},
            {"status": BillStatusType.UNPAID.value}
        ]

    final_query = {"$and": query} if query else {}
    print(final_query)
    lst_bills = list(bills.find(final_query).sort("invoice_date", -1))

    paid_count = bills.count_documents({"status": BillStatusType.PAID.value})
    unpaid_count = bills.count_documents({"status": BillStatusType.UNPAID.value})

    return render_template(
        "user/bill_payment.html",
        bills=lst_bills,
        start_date=start_date.strftime("%Y-%m-%d"),
        end_date=end_date.strftime("%Y-%m-%d"),
        status_filter=status_filter,
        paid_count=paid_count,
        unpaid_count=unpaid_count
    )

def insert_sample_bills():
    sample_bills = [
        {
            "account_id": 1,
            "type": "Electricity",
            "amount": 75000,
            "status": 0,  # UNPAID
            "invoice_date": dt(2024, 12, 1),
            "payment_date": None,
            "payment_method": None,
            "created_date": dt.now(),
            "created_by": 3,
            "modified_date": dt.now(),
            "modified_by": 3
        },
        {
            "account_id": 1,
            "type": "Water",
            "amount": 90000,
            "status": 1,  # PAID
            "invoice_date": dt(2024, 11, 28),
            "payment_date": dt(2024, 12, 1, 14, 30),
            "payment_method": "Visa",
            "created_date": dt.now(),
            "created_by": 3,
            "modified_date": dt.now(),
            "modified_by": 3
        }
    ]

    bills.insert_many(sample_bills)

@user_blueprint.route('/payment', methods=['POST'])
@login_required
@log_request()
@role_required(RoleType.USER.value)
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
                        {"account_number": account_number}
                    ]
                }
                account = accounts.find_one(find_query)

                if not account:
                    flash(messages_failure['account_not_found'], 'error')
                    return redirect(request.referrer)
                
                if float(account["balance"]) < float(amount):
                    flash(messages_failure['balance_not_enough'].format('pay the bill'), 'error')
                    return redirect(request.referrer)
                
                bills.update_one(
                    {"_id": int(bill_id)},
                    {
                        "$set": {
                            "status": BillStatusType.PAID.value,
                            "payment_method": payment_method,
                            "modified_date": dt.today(),
                            "modified_by": int(account["account_owner"])
                        }
                    }
                )

                accounts.update_one(
                    {"_id": int(account_id)},
                    {
                        "$set": {
                            "balance": account["balance"] - float(amount),
                            "modified_date": dt.today(),
                            "modified_by": int(account["account_owner"])
                        }
                    }
                )

                transaction_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
                trans = transaction.Transaction(
                    id = transaction_id,
                    sender = account['account_number'],
                    receiver = bill_id,
                    amount = float(amount),
                    currency = account['currency'],
                    message = f"Payment for {bill['bill_type']} bill of {bill['invoice_date'].strftime('%Y/%m/%d')}",
                    transaction_type = TransactionType.PAYMENT.value,
                    balance = account['balance'] - float(amount),
                    createdBy = int(account['account_owner']),
                    modified_by = int(account['account_owner'])
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
@log_request()
@role_required(RoleType.USER.value)
def investment_savings():
    account_id = int(session.get("account_id"))
    account = None
    currency_name = ''

    if account_id:
        account = accounts.find_one({'_id': account_id})
        currency_value = account['currency']

        match int(currency_value):
            case CurrencyType.USD.value:
                currency_name = CurrencyType.USD.name
            case CurrencyType.EUR.value:
                currency_name = CurrencyType.EUR.name
            case CurrencyType.VND.value:
                currency_name = CurrencyType.VND.name
            case _:
                currency_name = 'USD'

    today = dt.today()
    lst_investments = list(investments.find({}))

    for investment in lst_investments:
        lasted_update = dt.strptime(str(investment['modified_date']), '%Y-%m-%dT%H:%M:%S.%f').date() if "T" in str(
            investment['modified_date']) else dt.strptime(str(investment['modified_date']),
                                                          '%Y-%m-%d %H:%M:%S.%f').date()
        if lasted_update != today.date():
            current_investment_rate = round(random.uniform(-10, 10), 2)
            investments.update_one(
                {"_id": investment["_id"]},
                {
                    "$set": {
                        "current_rate": current_investment_rate,
                        "current_amount": investment['current_amount'] + investment['investment_amount'] * (
                            current_investment_rate) / 100,
                        "modified_date": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "modified_by": int(account["account_owner"])
                    }
                }
            )

    return render_template(
        "user/investment_savings.html",
        investment_date=today.date(),
        investments=lst_investments,
        currency=currency_name
    )

@user_blueprint.route('/add-investment-savings',methods=['POST'])
@login_required
@log_request()
@role_required(RoleType.USER.value)
def add_new_investment():
    try:
        account_id = int(session.get("account_id"))
        if account_id:
            account = accounts.find_one({'_id': account_id})
            if not account:
                flash(messages_failure['account_not_found'], 'error')
                return redirect(request.referrer)

            type_name = ''
            owner_id = account['account_owner']
            investment_name = request.form.get('investment_name')
            investment_type = request.form.get('investment_type')
            investment_amount = request.form.get('investment_amount')
            investment_date = request.form.get('investment_date')
            investment_rate = float(request.form.get('rate')) if request.form.get('rate') else 0

            if not investment_name or not investment_type or int(investment_type) < InvestmentType.STOCK.value or \
                not investment_amount or not investment_date:
                flash(messages_failure['must_input_value'], 'error')
                return redirect(request.referrer)
            
            if account["balance"] < float(investment_amount):
                flash(messages_failure['balance_not_enough'].format('investment/savings'), 'error')
                return redirect(request.referrer)

            match int(investment_type):
                case InvestmentType.STOCK.value:
                    type_name = InvestmentType.STOCK.name
                case InvestmentType.BONDS.value:
                    type_name = InvestmentType.BONDS.name
                case InvestmentType.REAL_ESTATE.value:
                    type_name = InvestmentType.REAL_ESTATE.name
                case InvestmentType.CRYPTO.value:
                    type_name = InvestmentType.CRYPTO.name

            investment_date = dt.strptime(investment_date, '%Y-%m-%d')
            investment_date = investment_date.replace(hour=0, minute=0, second=0, microsecond=0)

            investment_id = get_max_id(database=db, collection_name=CollectionType.INVESTMENTS_SAVINGS.value)
            investment = investment_model.Investment(
                id = investment_id,
                owner = int(owner_id),
                name = investment_name,
                type = type_name,
                investment_amount = float(investment_amount),
                investment_date = investment_date.isoformat(),
                rate = investment_rate,
                current_amount = float(investment_amount) + float(investment_amount)*investment_rate/100,
                createdBy = int(owner_id),
                modified_by = int(owner_id)
            )

            investments.insert_one(investment.to_json())
            investment = investments.find_one({'_id': investment_id})
            today = dt.today()

            accounts.update_one(
                {"_id": account_id},
                {
                    "$set": {
                        "balance": account["balance"] - float(investment_amount),
                        "modified_date": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "modified_by": int(owner_id)
                    }
                }
            )

            transaction_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
            trans = transaction.Transaction(
                id = transaction_id,
                sender = account['account_number'],
                receiver = investment_id,
                amount = float(investment_amount),
                currency = account['currency'],
                message = f"Investment for {investment['name']} of {dt.strptime(investment['investment_date'],'%Y-%m-%dT%H:%M:%S').strftime('%Y/%m/%d')}",
                transaction_type = TransactionType.INVESTMENT.value,
                balance = account['balance'] - float(investment_amount),
                createdBy = int(owner_id),
                modified_by = int(owner_id)
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
@log_request()
@role_required(RoleType.USER.value)
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

            edit_type_name = None
            set_query = {}
            amount = 0
            if int(edit_type) == InvestmentStatus.WITH_DRAW.value:
                set_query = {
                    "$set": {
                        "current_amount": 0,
                        "status": InvestmentStatus.WITH_DRAW.value,
                        "modified_date": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "modified_by": int(account["account_owner"])
                    }
                }
                edit_type_name = "Withdraw"
                amount = investment['current_amount']
            elif int(edit_type) == InvestmentStatus.CANCEL.value:
                set_query = {
                    "$set": {
                        "current_amount": 0,
                        "status": InvestmentStatus.CANCEL.value,
                        "modified_date": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "modified_by": int(account["account_owner"])
                    }
                }
                edit_type_name = "Cancel"
                amount = investment['investment_amount']
            account_balance = account['balance'] + amount

            accounts.update_one(
                {'_id': account_id},
                {
                    "$set": {
                        "balance": account_balance,
                        "modified_date": today.strftime('%Y-%m-%d %H:%M:%S.%f'),
                        "modified_by": int(account["account_owner"])
                    }
                }
            )

            trans_id = get_max_id(database=db, collection_name=CollectionType.TRANSACTIONS.value)
            trans = transaction.Transaction(
                id = trans_id,
                sender = "DHC Bank",
                receiver = account['account_number'],
                amount = amount,
                currency = account['currency'],
                message = f"{edit_type_name} from {investment['name']} of {dt.strptime(investment['investment_date'],'%Y-%m-%dT%H:%M:%S').strftime('%Y/%m/%d')}",
                transaction_type = TransactionType.WITHDRAWAL.value,
                balance = account_balance
            )
            transactions.insert_one(trans.to_json())

            investments.update_one(
                {'_id': int(investment_id)},
                set_query
            )
            flash(messages_success['withdraw_cancel_success'].format(edit_type_name), 'success')

    except Exception as e:
        print(e)
        flash(messages_failure['internal_server_error'], 'error')
    
    return redirect(request.referrer)

@user_blueprint.route('/card-management', methods=['GET'])
@login_required
@log_request()
@role_required(RoleType.USER.value)
def card_management():
    account_id = int(session.get("account_id"))
    account = accounts.find_one({"_id": account_id})
    user = users.find_one({"_id": int(account["account_owner"])})
    lst_card = []

    for card_id in list(user["cards"]):
        pipeline = [
            {"$match": {"_id": card_id}},
            {
                "$lookup": {
                    "from": "card_types",
                    "localField": "type",
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

    return render_template("user/card.html", cards=lst_card, user=user)
    
@user_blueprint.route('/lock-card/<card_id>', methods=['GET'])
@login_required
@log_request()
@role_required(RoleType.USER.value)
def lock_card(card_id):
    try:
        cards.update_one(
            { "_id": int(card_id)},
            {
                "$set": {
                    "is_deleted": DeletedType.DELETED.value,
                    "modified_by": int(session.get("account_id")),
                    "modified_date": dt.now()
                }
            }
        )
        flash(messages_success["locking_card_success"], "success")
    except Exception as e:
        print(e)
        flash(messages_failure["internal_server_error"], "error")

    return redirect(url_for("user.card_management"))
    
@user_blueprint.route('/unlock-card/<card_id>', methods=['GET'])
@login_required
@log_request()
@role_required(RoleType.USER.value)
def unlock_card(card_id):
    try:
        cards.update_one(
            { "_id": int(card_id)},
            {
                "$set": {
                    "is_deleted": DeletedType.AVAILABLE.value,
                    "modified_by": int(session.get("account_id")),
                    "modified_date": dt.now()
                }
            }
        )
        flash(messages_success["unlocking_card_success"], "success")
    except Exception as e:
        print(e)
        flash(messages_failure["internal_server_error"], "error")

    return redirect(url_for("user.card_management"))

@user_blueprint.route('/loan-management',methods=['GET'])
@log_request()
@role_required(RoleType.USER.value)
def loan_management():
    account_id = int(session.get("account_id"))
    lst_loan = list(loans.find({"owner": account_id}))
    return render_template("user/loan.html", loans=lst_loan)