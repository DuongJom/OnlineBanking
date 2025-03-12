import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer

from models import account, user, card as model_card , database
from message import messages_success, messages_failure
from helpers.helpers import issue_new_card, get_token, send_email, login_required, get_max_id
from enums.role_type import RoleType
from enums.card_type import CardType
from enums.collection import CollectionType
from app import app, mail

db = database.Database().get_db()
accounts = db[CollectionType.ACCOUNTS.value]
users = db[CollectionType.USERS.value]
branches = db[CollectionType.BRANCHES.value]
cards = db[CollectionType.CARDS.value]
card_types = db[CollectionType.CARD_TYPES.value]
transferMethods = db[CollectionType.TRANSFER_METHODS.value]
loginMethods = db[CollectionType.LOGIN_METHODS.value]

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('general/login.html', is_hidden=True)
    
    session.clear()
    username = request.form.get("username")
    password = request.form.get("password") 
    remember_me = request.form.get("remember_me")
    acc = accounts.find_one({"Username": username}) 

    if not acc or not check_password_hash(acc["Password"], password):
        flash(messages_failure["invalid_information"], 'error')
        return render_template('general/login.html')
        
    if remember_me:
        session.permanent = True
        current_app.config['PERMANENT_SESSION_LIFETIME'] = int(os.getenv('SESSION_LIFETIME'))
    else:
        session.permanent = False
        
    loggin_user = users.find_one({"_id":int(acc['AccountOwner'])})
    if loggin_user:
        session["sex"] = str(loggin_user['Sex'])
    session["account_id"] = str(acc["_id"])
        
    flash(messages_success['login_success'],'success')

    if acc["Role"] == RoleType.USER.value:
        return redirect("/")
    if acc["Role"] == RoleType.EMPLOYEE.value:
        return redirect("/employee/home")
    return redirect(url_for('admin_account.admin_account', page_no=1))

@account_blueprint.route('/register', methods=['GET','POST'])
def register():
    card_info = issue_new_card()
    if request.method == 'GET':
        branch_list = branches.find()
        return render_template('general/register.html', 
                               branch_list=branch_list, 
                               card_info=card_info,
                               is_hidden = True)
    
    # get the data from post request
    username = request.form['username']
    fullName = request.form['fullname']
    branch_id = request.form['branch']
    password = request.form['password']
    country = request.form['country']
    city = request.form['city']
    distinct = request.form['district']
    ward = request.form['ward']
    street = request.form['street']
    address = f'{street}, {ward}, {distinct}, {city}, {country}'
    transfer_method_ids = [int(id) for id in request.form.getlist('transferMethod') if id.isdigit()]
    confirm_password = request.form['confirmPassword']
    phone = request.form['phone']
    login_method_ids = [int(id) for id in request.form.getlist('loginMethod') if id.isdigit()]
    email = request.form['email']
    sex = request.form['gender']

    # check if user input email and password or not
    error_message = None
    if password != confirm_password:
        error_message = messages_failure['password_not_matched']

    # check if email or username already exist
    is_exist_username = True if accounts.find_one({"Username": username}) else False
    is_exist_email = True if users.find_one({"Email": email}) else False
    is_exist_phone = True if users.find_one({"Phone": phone}) else False

    if is_exist_username:
        error_message = messages_failure['username_existed'].format(username) 
    elif is_exist_email:
        error_message = messages_failure['email_existed'].format(email) 
    elif is_exist_phone:
        error_message = messages_failure['phone_existed'].format(phone)
        
    if error_message:
        flash(error_message, 'error')
        return redirect(url_for("account.register"))

    # insert the document to the collection if there is no error
    new_card_id = get_max_id(database=db, collection_name=CollectionType.CARDS.value)
    new_card = model_card.Card(
        id=new_card_id, 
        cardNumber=card_info['cardNumber'], 
        cvv=card_info['cvvNumber'], 
        type=CardType.CREDITS.value
    )

    cards.insert_one(new_card.to_json())

    # insert new user into database
    new_user_id = get_max_id(database=db, collection_name=CollectionType.USERS.value)
    new_user = user.User(
        id=new_user_id, 
        name=fullName, 
        sex=int(sex), 
        address=address.strip(), 
        phone=phone, 
        email=email, 
        card=[new_card_id,]
    )
    users.insert_one(new_user.to_json())

    # insert new account into database
    new_account_id = get_max_id(database=db, collection_name=CollectionType.ACCOUNTS.value)
    new_account = account.Account(
        id=new_account_id,
        accountNumber=card_info['accountNumber'], 
        branch=int(branch_id), 
        user=new_user_id, 
        username=username, 
        password=password, 
        role=RoleType.USER.value, 
        transferMethod=transfer_method_ids, 
        loginMethod=login_method_ids
    )
    accounts.insert_one(new_account.to_json())

    flash(messages_success['register_success'], 'success')
    return redirect(url_for("account.login"))
    
@account_blueprint.route('/view-profile',  methods=['GET', 'POST'])
@login_required
def view_profile():
    if request.method == "GET":
        if session.get("account_id"):
            account_id = int(session.get("account_id"))
            account = accounts.find_one({"_id": account_id})
            lst_cards = []
            owner = None

            if account:
                branch = branches.find_one({"_id": int(account["Branch"])})
                owner = users.find_one({"_id": int(account["AccountOwner"])})
                if owner and len(list(owner['Card'])) != 0:
                    for card_id in list(owner['Card']):
                        card = cards.find_one({"_id": int(card_id)})
                        if card:
                            card_type = None
                            if int(card['Type']) == CardType.CREDITS.value:
                                card_type = CardType.CREDITS.name.capitalize()
                            elif int(card['Type']) == CardType.DEBITS.value:
                                card_type = CardType.DEBITS.name.capitalize()

                            lst_cards.append({
                                'card_info': card,
                                'card_type': card_type
                            })
            return render_template("general/view_profile.html", account=account, cards=lst_cards, owner=owner, branch=branch)
        
    new_email = request.form.get("email")
    new_phone = request.form.get("phone")
    new_address = request.form.get("address")
    new_username = request.form.get("username")
    current_email = request.form.get("current_email")
    current_phone = request.form.get("current_phone")
    current_username = request.form.get("current_username")
    password = request.form.get("password")
    current_account = accounts.find_one({"_id": int(session.get("account_id"))})
    current_user = users.find_one({"_id": int(current_account["AccountOwner"])})

    error_message = None
    if not check_password_hash(current_account["Password"], password):
        error_message = messages_failure["password_not_matched"]    
    elif users.find_one({"Email": new_email}) is not None and current_email != new_email:
        error_message = messages_failure['email_existed'].format(new_email) 
    elif users.find_one({"Phone": new_phone}) is not None and current_phone != new_phone:
        error_message = messages_failure["phone_existed"].format(new_phone)
    elif accounts.find_one({"Username": new_username}) is not None and current_username != new_username:
        error_message = messages_failure['username_existed'].format(new_username) 

    if error_message:
        flash(error_message, "error")
        return redirect("/view-profile")

    users.update_one(
        {"Email": current_user["Email"]},
        {
            "$set": {
                "Email": new_email, 
                "Phone": new_phone, 
                "Address": new_address
            }
        }
    )
             
    accounts.update_one(
        {"_id": current_account["_id"]},
        {"$set": {"Username": new_username}}
    )

    flash(messages_success["update_success"].format("information"), "success");   
    return redirect("/view-profile")

@account_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("account.login"))

@account_blueprint.route('/confirm-email', methods=['GET', 'POST'])
def confirm_email():
    if request.method == 'GET':
        return render_template('email/confirm_email.html')
    
    user_email = request.form.get('email')
    # verify if user exist, send reset password page to the user's email
    user = users.find_one({'Email': user_email})

    if not user:
        flash(messages_failure['invalid_email'].format(user_email), 'error')
        return render_template('email/confirm_email.html')
        
    token = get_token(app=app, user_email=user_email, salt=app.salt)
    subject = "Reset Password"
    recover_url = url_for('account.reset_password',token=token, _external=True)
    html = render_template('email/activate.html',recover_url=recover_url)
    attachments = [{'path': './static/img/bank.png', 'filename':'bank.png', 'mime_type': 'image/png'}]
    send_email(app=app, mail=mail, recipients=[user_email], subject=subject, html=html, attachments=attachments)
    flash(messages_success['link_sent'].format(user_email), 'success')
    return redirect(url_for('account.login'))

@account_blueprint.route('/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if request.method == 'GET':
        return render_template('general/reset_password.html', token=token)
        
    try:
        ts = URLSafeTimedSerializer(app.secret_key)
        user_email = ts.loads(token, salt=app.salt, max_age=86400)
        new_password = generate_password_hash(request.form.get('password'))
        user = users.find_one({'Email': user_email},{'_id':1})

        update_account_result = accounts.update_one(
            {'AccountOwner': user["_id"]},
            {"$set": {"Password": new_password}}
        )
                
        # Check if the update was successful
        if update_account_result.modified_count > 0:
            flash(messages_success['update_success'].format('password'), 'success')
            return redirect(url_for('account.login'))
                
        flash(messages_failure['document_not_found'], 'error')
    except Exception as e:
        print(e)
        flash(messages_failure['token_expired'], 'error')
        return redirect(url_for('account.login'))
    return redirect(url_for('account.reset_password', token=token))

@account_blueprint.route('/change-password', methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("general/change_password.html", is_hidden=True)
        
    current_password = request.form.get("current_password")
    new_password = generate_password_hash(request.form.get("new_password"))
    confirm_password = request.form.get("confirmPassword")
    current_user = accounts.find_one({"_id": int(session.get("account_id"))})

    if not check_password_hash(current_user["Password"], current_password):
        flash(messages_failure["invalid_password"], "error")
        return redirect("/change-password")
        
    if not check_password_hash(new_password, confirm_password):
        flash(messages_failure["password_not_matched"], "error")
        return redirect("/change-password")
        
    accounts.update_one(
        {'_id': int(session.get("account_id"))},
        {"$set": {"Password": new_password}
    })

    session.clear()
    flash(messages_success['update_success'].format('password'), 'success')
    return redirect("/login")


