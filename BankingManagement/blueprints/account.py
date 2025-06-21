import os
from flask import (
    Blueprint, render_template, redirect, url_for, flash,
    request, session, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from itsdangerous import URLSafeTimedSerializer

from models import account, user, card as model_card
from message import messages_success, messages_failure
from helpers.helpers import issue_new_card, get_token, send_email, get_max_id
from decorators import login_required, role_required, log_request
from enums.role_type import RoleType
from enums.card_type import CardType
from enums.collection import CollectionType
from enums.deleted_type import DeletedType
from app import app, mail
from flask_caching import Cache
from init_database import (
    db, accounts, users, branches, cards
)

cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})
cache.init_app(app)

HASH_PASSWORD_METHOD = 'pbkdf2:sha256'
SALT_LENGTH = 16
MAX_AGE_TIME_SERIALIZER = 86400

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
@log_request()
def login():
    if request.method == 'GET':
        return render_template("general/login.html")

    session.clear()
    form_data = request.form
    username = form_data.get("username")
    password = form_data.get("password")
    remember_me = form_data.get("remember_me")

    acc = accounts.find_one(
        {"username": username, "is_deleted": DeletedType.AVAILABLE.value},
        {"_id": 1, "username": 1, "password": 1, "role": 1, "account_owner": 1}
    )

    if not acc or not check_password_hash(acc["password"], password):
        flash(messages_failure["invalid_information"], "error")
        return render_template("general/login.html")

    session.permanent = bool(remember_me)

    if session.permanent:
        current_app.config['PERMANENT_SESSION_LIFETIME'] = int(os.getenv('SESSION_LIFETIME'))

    if not acc['account_owner']:
        flash(messages_failure["account_owner_not_found"], 'error')
        return redirect(url_for("account.login"))

    logging_user = users.find_one(
        {"_id": int(acc['account_owner'])},
        {"name": 1, "sex": 1, "avatar": 1}
    )

    if logging_user:
        session["sex"] = str(logging_user['sex'])

    session["account_id"] = str(acc["_id"])
    session["avatar"] = logging_user["avatar"]
    session["fullname"] = logging_user["name"] if logging_user["name"] != "" else acc["username"]
    flash(messages_success['login_success'], 'success')

    return redirect({
        RoleType.ADMIN.value: "/admin/home",
        RoleType.EMPLOYEE.value: "/employee/home",
        RoleType.USER.value: "/"
    }.get(acc["role"], "/"))

@account_blueprint.route('/register', methods=['GET', 'POST'])
@log_request()
def register():
    card_info = issue_new_card()

    if request.method == 'GET':
        branch_list = cache.get("branch_list")
        if branch_list is None:
            branch_list = list(branches.find({}, {"_id": 1, "branch_name": 1, "address": 1}))
            cache.set("branch_list", branch_list, timeout=300)
        return render_template("general/register.html", branch_list=branch_list, card_info=card_info)

    form_data = request.form
    avatar_file = request.files.get("avatar")
    username = form_data['username']
    full_name = form_data['fullname']
    branch_id = form_data['branch']
    password = form_data['password']
    confirm_password = form_data['confirm_password']
    address = ", ".join([form_data.get(k, '').strip() for k in ['street', 'ward', 'district', 'city', 'country']])
    transfer_method_ids = [int(transfer_method_id) for transfer_method_id in form_data.getlist('transfer_method') if transfer_method_id.isdigit()]
    login_method_ids = [int(login_method_id) for login_method_id in form_data.getlist('login_method') if login_method_id.isdigit()]
    phone = form_data['phone']
    email = form_data['email']
    sex = form_data['gender']

    if password != confirm_password:
        flash(messages_failure['password_not_matched'], 'error')
        return redirect(url_for("account.register"))

    if accounts.find_one({"username": username}):
        flash(messages_failure['username_existed'].format(username), 'error')
        return redirect(url_for("account.register"))

    if users.find_one({"email": email}):
        flash(messages_failure['email_existed'].format(email), 'error')
        return redirect(url_for("account.register"))

    if users.find_one({"phone": phone}):
        flash(messages_failure['phone_existed'].format(phone), 'error')
        return redirect(url_for("account.register"))

        # Process avatar
    avatar_filename = None
    if avatar_file and avatar_file.filename:
        filename = secure_filename(avatar_file.filename)
        upload_path = os.path.join(current_app.root_path, 'static', 'uploads', filename)
        os.makedirs(os.path.dirname(upload_path), exist_ok=True)
        avatar_file.save(upload_path)
        avatar_filename = filename

    new_card_id = get_max_id(db, CollectionType.CARDS.value)
    cards.insert_one(model_card.Card(
        id=new_card_id,
        card_number=card_info['card_number'],
        cvv_number=card_info['cvv_number'],
        type=CardType.CREDITS.value
    ).to_json())

    new_user_id = get_max_id(db, CollectionType.USERS.value)
    users.insert_one(user.User(
        id=new_user_id,
        name=full_name,
        sex=int(sex),
        address=address.strip(),
        phone=phone,
        email=email,
        avatar=avatar_filename,
        card=[new_card_id]
    ).to_json())

    new_account_id = get_max_id(db, CollectionType.ACCOUNTS.value)
    accounts.insert_one(account.Account(
        id=new_account_id,
        account_number=card_info['account_number'],
        branch_id=int(branch_id),
        user=new_user_id,
        username=username,
        password=password,
        role=RoleType.USER.value,
        transfer_method=transfer_method_ids,
        login_method=login_method_ids
    ).to_json())

    flash(messages_success['register_success'], 'success')
    return redirect(url_for("account.login"))

@account_blueprint.route('/view-profile', methods=['GET', 'POST'])
@login_required
@log_request()
@role_required(RoleType.ADMIN.value, RoleType.EMPLOYEE.value, RoleType.USER.value)
def view_profile():
    account_id = int(session.get("account_id"))
    account_doc = accounts.find_one({"_id": account_id})

    if request.method == "GET":
        branch = branches.find_one({"_id": account_doc["branch_id"]}) if account_doc else None
        owner = users.find_one({"_id": account_doc["account_owner"]}) if account_doc else None
        lst_cards = []

        if owner:
            card_ids = [int(cid) for cid in owner.get('card', [])]

            for card in cards.find({"_id": {"$in": card_ids}}):
                card_type = CardType(card['type']).name.capitalize()
                lst_cards.append({'card_info': card, 'card_type': card_type})

        return render_template(
            "general/view_profile.html",
            account=account_doc,
            cards=lst_cards,
            owner=owner,
            branch=branch
        )

    form_data = request.form
    user_doc = users.find_one({"_id": account_doc["account_owner"]})

    if not check_password_hash(account_doc["password"], form_data.get("password")):
        flash(messages_failure["password_not_matched"], "error")
        return redirect("/view-profile")

    for field, msg, col, key in [
        ("email", 'email_existed', users, 'email'),
        ("phone", 'phone_existed', users, 'phone'),
        ("username", 'username_existed', accounts, 'username')
    ]:
        if form_data.get(field) != form_data.get(f"current_{field}") and col.find_one({key: form_data.get(field)}):
            flash(messages_failure[msg].format(form_data.get(field)), "error")
            return redirect("/view-profile")

    users.update_one(
        {"_id": user_doc["_id"]},
        {
            "$set": {
                "email": form_data.get("email"),
                "phone": form_data.get("phone"),
                "address": form_data.get("address")
            }
        }
    )

    accounts.update_one(
        {"_id": account_doc["_id"]},
        {
            "$set": {
                "username": form_data.get("username")
            }
        }
    )

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
    user_doc = users.find_one(
        {'email': email},
        {'_id': 1}
    )

    if not user_doc:
        flash(messages_failure['invalid_email'].format(email), 'error')
        return render_template('email/confirm_email.html')

    token = get_token(app=app, user_email=email, salt=app.salt)
    html = render_template(
        template_name_or_list='email/activate.html',
        recover_url=url_for(endpoint='account.reset_password', token=token, _external=True)
    )
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
        time_serializer = URLSafeTimedSerializer(app.secret_key)
        email = time_serializer.loads(token, salt=app.salt, max_age=MAX_AGE_TIME_SERIALIZER)
        hashed_password = generate_password_hash(
            password=request.form.get('password'),
            method=HASH_PASSWORD_METHOD,
            salt_length=SALT_LENGTH
        )

        user_doc = users.find_one(
            {'email': email},
            {'_id': 1}
        )

        update_result = accounts.update_one(
            {"account_owner": user_doc["_id"]},
            {
                "$set": {
                    "password": hashed_password
                }
            }
        )

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
    current_password = form.get("current_password")
    new_password = form.get("new_password")
    confirm_password = form.get("confirm_password")

    if new_password != confirm_password:
        flash(messages_failure["password_not_matched"], "error")
        return redirect("/change-password")

    account_doc = accounts.find_one({"_id": int(session.get("account_id"))})

    if not check_password_hash(account_doc["password"], current_password):
        flash(messages_failure["invalid_password"], "error")
        return redirect("/change-password")

    hashed_password = generate_password_hash(
        password=new_password,
        method=HASH_PASSWORD_METHOD,
        salt_length=SALT_LENGTH
    )

    accounts.update_one(
        {'_id': account_doc["_id"]},
        {
            "$set": {
                "password": hashed_password
            }
        }
    )

    session.clear()
    flash(messages_success['update_success'].format('password'), 'success')
    return redirect("/login")