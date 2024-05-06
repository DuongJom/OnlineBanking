from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, Response
from werkzeug.security import check_password_hash, generate_password_hash
from bson import ObjectId
from datetime import datetime
from models import account, user, card as model_card , database
from message import messages_success, messages_failure
from helpers import issueNewCard, get_token, send_email, ts, login_required
from SysEnum import RoleType
from app import app

db = database.Database().get_db()
accounts = db['accounts']
users = db['users']
branches = db['branches']
cards = db['cards']
transferMethods = db['transferMethods']
loginMethods = db['loginMethods']
services = db['services']

account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password") 
        remember_me = request.form.get("remember_me")
        
        acc = accounts.find_one({"Username": username}) 

        if acc is None or not check_password_hash(acc["Password"], password):
            flash(messages_failure["invalid_information"], 'error')
            return render_template('login.html')
        
        if remember_me:
            session.permanent = True
            current_app.config['PERMANENT_SESSION_LIFETIME'] = 1209600  # 2 weeks in seconds
        else:
            session.permanent = False
            session["sex"] = str(acc['AccountOwner']['Sex'])
        session["account_id"] = str(acc["_id"])
        
        flash(messages_success['login_success'],'success')
        if acc["Role"] == RoleType.USER.value:
            return redirect("/")
        elif acc["Role"] == RoleType.EMPLOYEE.value:
            return redirect("/employee/home")
        else:
            return redirect("/admin/home")
        
    return render_template('login.html')

@account_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # get the data from post request
        username = request.form['username']
        fullName = request.form['fullName']
        branch_id = request.form['branch']
        password = request.form['password']
        address = request.form['address']
        transferMethod_id = request.form['transferMethod']
        confirmPassword = request.form['confirmPassword']
        phone = request.form['phone']
        loginMethod_id = request.form['loginMethod']
        email = request.form['email']
        sex = request.form['sex']
        service_id = request.form['service']
        card = request.form['card']
        accountNumber = request.form['accountNumber']
        cvvNumber = request.form['cvvNumber']

        # check if user input email and password or not, get error message from message.py
        error = None
        if password != confirmPassword:
            error = messages_failure['password_not_matched']

        # check if email or username already exist, using .format() to format error message
        existUsername = accounts.find_one({"Username": username})
        existEmail = users.find_one({"Email": email})
        existPhone = users.find_one({"Phone": phone})

        if existUsername:
            error = messages_failure['username_existed'].format(username) 
        elif existEmail:
            error = messages_failure['email_existed'].format(email) 
        elif existPhone:
            error = messages_failure['phone_existed'].format(phone)
        
        if error:
            flash(error, 'error')
            return redirect(url_for("account.register"))

        # insert the document to the collection if there is no error

        new_card = model_card.Card(cardNumber=card, cvv=cvvNumber)

        cards.insert_one(new_card.to_json())

        # insert new user into database
        new_user = user.User(name=fullName, sex=sex, address=address, phone=phone, email=email, card=new_card.to_json())
        users.insert_one(new_user.to_json())

        # get data from database
        branch = branches.find_one({"_id": branch_id})
        transferMethod = transferMethods.find_one({"_id": transferMethod_id})
        loginMethod = loginMethods.find_one({"_id": loginMethod_id})
        service = services.find_one({"_id": service_id})

        # insert new account into database
        new_account = account.Account(accountNumber=accountNumber, branch=branch, user=new_user.to_json(), 
                                        username=username, password=password, role=RoleType.USER.value, 
                                        transferMethod=[transferMethod], 
                                        loginMethod=[loginMethod], service=[service])
        accounts.insert_one(new_account.to_json())

        flash(messages_success['success'], 'success')
        return redirect(url_for("account.login"))
    
    elif request.method == 'GET':
        branch_list = branches.find()
        loginMethod_list = loginMethods.find()
        transferMethod_list = transferMethods.find()
        service_list = services.find()
        card_info = issueNewCard()
        return render_template('register.html', branch_list=branch_list, loginMethod_list=loginMethod_list,
                               transferMethod_list=transferMethod_list, service_list=service_list, card_info=card_info)
    
@account_blueprint.route('/view-profile',  methods=['GET', 'POST'])
@login_required
def view_profile():
    if request.method == "GET":
        if session.get("account_id"):
            account_id = ObjectId(session.get("account_id"))
            account = accounts.find_one({"_id": account_id})
            expired_date = None
            if account and account['AccountOwner']['Card']:
                expired_date = datetime.fromisoformat(account['AccountOwner']['Card']['ExpiredDate']).date()
            return render_template("view_profile.html", account = account, expired_date = expired_date)
    elif request.method == "POST":
        new_email = request.form.get("email")
        new_phone = request.form.get("phone")
        new_address = request.form.get("address")
        new_username = request.form.get("username")
        current_email = request.form.get("current_email")
        current_phone = request.form.get("current_phone")
        current_username = request.form.get("current_username")
        password = request.form.get("password")

        current_account = accounts.find_one({"_id": ObjectId(session.get("account_id"))})

        error = None
        if not check_password_hash(current_account["Password"], password):
            error = messages_failure["password_not_matched"]    
        elif users.find_one({"Email": new_email}) is not None and current_email != new_email:
            error = messages_failure['email_existed'].format(new_email) 
        elif users.find_one({"Phone": new_phone}) is not None and current_phone != new_phone:
            error = messages_failure["phone_existed"].format(new_phone)
        elif accounts.find_one({"Username": new_username}) is not None and current_username != new_username:
            error = messages_failure['username_existed'].format(new_username) 

        if error:
            flash(error, "error")
            return redirect("/view-profile")

        users.update_one(
            {"Email": current_account["AccountOwner"]["Email"]},
            {
                "$set": {
                    "Email": new_email, 
                    "Phone": new_phone, 
                    "Address": new_address
                }
            }
        )
        
        updated_user = users.find_one({"Email": new_email}, {"_id":0})
             
        accounts.update_one(
            {"_id": current_account["_id"]},
            {
                "$set": {
                    "Username": new_username, 
                    "AccountOwner": updated_user
                }
            }
        )

        flash(messages_success["update_success"].format("information"), "success");   
        return redirect("/view-profile")



@account_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("account.login"))

@account_blueprint.route('/confirm-email', methods=['GET', 'POST'])
def confirm_email():
    if request.method == 'POST':
        user_email = request.form.get('email')
        # verify if user exist, send reset password page to the user's email
        exist_user = users.find_one({'Email': user_email})

        if exist_user is None:
            flash(messages_failure['invalid_email'].format(user_email), 'error')
            return render_template('confirm_email.html')
        
        token = get_token(user_email, salt=app.salt)
        subject = "Reset Password"
        recover_url = url_for('account.reset_password',token=token, _external=True)
        html = render_template('email/activate.html',recover_url=recover_url)
        attachments = [{'path': './static/img/bank.png', 'filename':'bank.png', 'mime_type': 'image/png'}]
        send_email(user_email, subject, html, attachments=attachments)
        flash(messages_success['link_sent'].format(user_email), 'success')
        return redirect(url_for('account.login'))
    return render_template('confirm_email.html')

@account_blueprint.route('/reset-password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if request.method == 'POST':
        try:
            user_email = ts.loads(token, salt=app.salt, max_age=86400)
            new_password = generate_password_hash(request.form.get('password'))
            exist_user = users.find_one({'Email': user_email},{'_id':0})

            update_password = accounts.update_one(
                {'AccountOwner': exist_user},
                {
                    "$set": {
                        "Password": new_password
                    }
                }
            )
                
            # Check if the update was successful
            if update_password.modified_count > 0:
                flash(messages_success['update_success'].format('password'), 'success')
                return redirect(url_for('account.login'))
                
            flash(messages_failure['document_not_found'], 'error')
            return redirect(url_for('account.reset_password', token=token))
        except:
            flash(messages_failure['token_expired'], 'error')
            return redirect(url_for('account.login'))
    return render_template('reset_password.html', token=token)

