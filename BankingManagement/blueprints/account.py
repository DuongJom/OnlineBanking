import os
from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    request, session, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer

from models import account, user, card as model_card, database
from message import messages_success, messages_failure
from helpers.helpers import issue_new_card, get_token, send_email, get_max_id
from decorators import login_required, role_required, log_request
from enums.role_type import RoleType
from enums.card_type import CardType
from enums.collection import CollectionType
from enums.deleted_type import DeletedType
from app import app, mail

# MongoDB Collections
db = database.Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
users = db[CollectionType.USERS.value]
branches = db[CollectionType.BRANCHES.value]
cards = db[CollectionType.CARDS.value]
card_types = db[CollectionType.CARD_TYPES.value]
transfer_methods = db[CollectionType.TRANSFER_METHODS.value]
login_methods = db[CollectionType.LOGIN_METHODS.value]

account_blueprint = Blueprint('account', __name__)


@account_blueprint.route('/login', methods=['GET', 'POST'])
@log_request()
def login():
    if request.method == 'GET':
        return render_template('general/login.html')

    session.clear()
    username = request.form.get("username")
    password = request.form.get("password")
    remember_me = request.form.get("remember_me")
    acc = accounts.find_one({"Username": username, "IsDeleted": DeletedType.AVAILABLE.value})

    if not acc or not check_password_hash(acc["Password"], password):
        flash(messages_failure["invalid_information"], 'error')
        return render_template('general/login.html')

    session.permanent = bool(remember_me)

    if session.permanent:
        current_app.config['PERMANENT_SESSION_LIFETIME'] = int(os.getenv('SESSION_LIFETIME'))

    loggin_user = users.find_one({"_id": int(acc['AccountOwner'])})

    if loggin_user:
        session["sex"] = str(loggin_user['Sex'])

    session["account_id"] = str(acc["_id"])
    flash(messages_success['login_success'], 'success')

    return redirect({
        RoleType.ADMIN.value: "/admin/home",
        RoleType.EMPLOYEE.value: "/employee/home",
        RoleType.USER.value: "/"
    }.get(acc["Role"], "/"))


@account_blueprint.route('/register', methods=['GET', 'POST'])
@log_request()
def register():
    card_info = issue_new_card()

    if request.method == 'GET':
        branch_list = branches.find()
        return render_template('general/register.html', branch_list=branch_list, card_info=card_info)

    form = request.form
    username = form['username']
    full_name = form['fullname']
    branch_id = form['branch']
    password = form['password']
    confirm_password = form['confirmPassword']
    address = f"{form['street']}, {form['ward']}, {form['district']}, {form['city']}, {form['country']}"
    transfer_method_ids = [int(i) for i in form.getlist('transferMethod') if i.isdigit()]
    login_method_ids = [int(i) for i in form.getlist('loginMethod') if i.isdigit()]
    phone = form['phone']
    email = form['email']
    sex = form['gender']

    if password != confirm_password:
        flash(messages_failure['password_not_matched'], 'error')
        return redirect(url_for("account.register"))

    if accounts.find_one({"Username": username}):
        flash(messages_failure['username_existed'].format(username), 'error')
        return redirect(url_for("account.register"))

    if users.find_one({"Email": email}):
        flash(messages_failure['email_existed'].format(email), 'error')
        return redirect(url_for("account.register"))

    if users.find_one({"Phone": phone}):
        flash(messages_failure['phone_existed'].format(phone), 'error')
        return redirect(url_for("account.register"))

    new_card_id = get_max_id(db, CollectionType.CARDS.value)
    new_card = model_card.Card(id=new_card_id, cardNumber=card_info['cardNumber'], cvv=card_info['cvvNumber'], type=CardType.CREDITS.value)
    cards.insert_one(new_card.to_json())

    new_user_id = get_max_id(db, CollectionType.USERS.value)
    new_user = user.User(id=new_user_id, name=full_name, sex=int(sex), address=address.strip(), phone=phone, email=email, card=[new_card_id])
    users.insert_one(new_user.to_json())

    new_account_id = get_max_id(db, CollectionType.ACCOUNTS.value)
    new_account = account.Account(id=new_account_id, accountNumber=card_info['accountNumber'], branch=int(branch_id), user=new_user_id, username=username, password=password, role=RoleType.USER.value, transferMethod=transfer_method_ids, loginMethod=login_method_ids)
    accounts.insert_one(new_account.to_json())

    flash(messages_success['register_success'], 'success')
    return redirect(url_for("account.login"))


@account_blueprint.route('/view-profile', methods=['GET', 'POST'])
@login_required
@log_request()
@role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value, RoleType.USER.value)
def view_profile():
    if request.method == "GET":
        account_id = int(session.get("account_id"))
        acc = accounts.find_one({"_id": account_id})
        branch = branches.find_one({"_id": int(acc["Branch"])}) if acc else None
        owner = users.find_one({"_id": int(acc["AccountOwner"])}) if acc else None

        lst_cards = []

        if owner:
            for card_id in owner.get('Card', []):
                card = cards.find_one({"_id": int(card_id)})

                if card:
                    card_type = CardType(card['Type']).name.capitalize()
                    lst_cards.append({'card_info': card, 'card_type': card_type})

        return render_template("general/view_profile.html", account=acc, cards=lst_cards, owner=owner, branch=branch)

    form = request.form
    account_id = int(session.get("account_id"))
    acc = accounts.find_one({"_id": account_id})
    usr = users.find_one({"_id": acc["AccountOwner"]})

    if not check_password_hash(acc["Password"], form.get("password")):
        flash(messages_failure["password_not_matched"], "error")
        return redirect("/view-profile")

    for field, msg, col, key in [
        ("email", 'email_existed', users, 'Email'),
        ("phone", 'phone_existed', users, 'Phone'),
        ("username", 'username_existed', accounts, 'Username')
    ]:
        if form.get(field) != form.get(f"current_{field}") and col.find_one({key: form.get(field)}):
            flash(messages_failure[msg].format(form.get(field)), "error")
            return redirect("/view-profile")

    users.update_one({"_id": usr["_id"]}, {"$set": {"Email": form.get("email"), "Phone": form.get("phone"), "Address": form.get("address")}})
    accounts.update_one({"_id": acc["_id"]}, {"$set": {"Username": form.get("username")}})

    flash(messages_success["update_success"].format("information"), "success")
    return redirect("/view-profile")

@account_blueprint.route("/logout")
@log_request()
@role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value, RoleType.USER.value)
def logout():
    session.clear()
    return redirect(url_for("account.login"))


@account_blueprint.route('/confirm-email', methods=['GET', 'POST'])
@log_request()
def confirm_email():
    if request.method == 'GET':
        return render_template('email/confirm_email.html')

    email = request.form.get('email')
    usr = users.find_one({'Email': email})
    if not usr:
        flash(messages_failure['invalid_email'].format(email), 'error')
        return render_template('email/confirm_email.html')

    token = get_token(app=app, user_email=email, salt=app.salt)
    html = render_template('email/activate.html', recover_url=url_for('account.reset_password', token=token, _external=True))
    attachments = [{'path': './static/img/bank.png', 'filename': 'bank.png', 'mime_type': 'image/png'}]
    send_email(app=app, mail=mail, recipients=[email], subject="Reset Password", html=html, attachments=attachments)

    flash(messages_success['link_sent'].format(email), 'success')
    return redirect(url_for('account.login'))


@account_blueprint.route('/reset-password/<token>', methods=["GET", "POST"])
@log_request()
def reset_password(token):
    if request.method == 'GET':
        return render_template('general/reset_password.html', token=token)

    try:
        ts = URLSafeTimedSerializer(app.secret_key)
        email = ts.loads(token, salt=app.salt, max_age=86400)
        hashed_pw = generate_password_hash(request.form.get('password'), method='pbkdf2:sha256', salt_length=16)
        usr = users.find_one({'Email': email}, {'_id': 1})

        update_result = accounts.update_one({'AccountOwner': usr["_id"]}, {"$set": {"Password": hashed_pw}})
        if update_result.modified_count:
            flash(messages_success['update_success'].format('password'), 'success')
            return redirect(url_for('account.login'))

        flash(messages_failure['document_not_found'], 'error')
    except Exception as e:
        print(e)
        flash(messages_failure['token_expired'], 'error')

    return redirect(url_for('account.reset_password', token=token))


@account_blueprint.route('/change-password', methods=["GET", "POST"])
@login_required
@log_request()
@role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value, RoleType.USER.value)
def change_password():
    if request.method == "GET":
        return render_template("general/change_password.html")

    form = request.form
    current_pw = form.get("current_password")
    new_pw = form.get("new_password")
    confirm_pw = form.get("confirmPassword")

    if new_pw != confirm_pw:
        flash(messages_failure["password_not_matched"], "error")
        return redirect("/change-password")

    acc = accounts.find_one({"_id": int(session.get("account_id"))})
    if not check_password_hash(acc["Password"], current_pw):
        flash(messages_failure["invalid_password"], "error")
        return redirect("/change-password")

    hashed_pw = generate_password_hash(new_pw, method='pbkdf2:sha256', salt_length=16)
    accounts.update_one({'_id': acc["_id"]}, {"$set": {"Password": hashed_pw}})

    session.clear()
    flash(messages_success['update_success'].format('password'), 'success')
    return redirect("/login")