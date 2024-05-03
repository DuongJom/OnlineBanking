from werkzeug.security import check_password_hash, generate_password_hash
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, Response
from werkzeug.security import check_password_hash, generate_password_hash
from bson import ObjectId
from datetime import datetime
from models import account, user, card as model_card , database
from message import messages
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
        password = request.form.get('password') 
        remember_me = request.form.get("remember_me")
        
        acc = accounts.find_one({"Username": username}) 

        if acc is None:
            flash(messages["invalid_information"], 'error')
            return render_template('login.html')
        
        if not check_password_hash(acc["Password"], password):
            flash(messages['invalid_information'], 'error')
            return render_template('login.html')
        
        if remember_me:
            session.permanent = True
            current_app.config['PERMANENT_SESSION_LIFETIME'] = 1209600  # 2 weeks in seconds
            session["userId"] = str(acc["_id"])
        else:
            session.permanent = False
            session["userId"] = str(acc["_id"])

            session["sex"] = str(acc['AccountOwner']['Sex'])
        
        flash(messages['login_success'],'success')
        if acc["Role"] == RoleType.USER.value:
            return redirect("/")
        elif acc["Role"] == RoleType.EMPLOYEE.value:
            return redirect("/employee")
        else:
            return redirect("/admin")
    session.clear()
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
            error = messages['password_not_matched']

        # check if email or username already exist, using .format() to format error message
        existUsername = accounts.find_one({"Username": username})
        existEmail = users.find_one({"Email": email})

        if existUsername:
            error = messages['username_existed'].format(username) 
        elif existEmail:
            error = messages['email_existed'].format(email) 
        
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
        service = services.find_one({"_id": service_id})

        # insert new account into database
        new_account = account.Account(accountNumber=accountNumber, branch=branch, user=new_user.to_json(), 
                                        username=username, password=password, role=RoleType.USER.value, 
                                        transferMethod=[transferMethod], 
                                        loginMethod=[loginMethod], service=[service])
        accounts.insert_one(new_account.to_json())

        flash(messages['success'].format(), 'success')
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
        userId = ObjectId(session.get("userId"))
        account = accounts.find_one({"_id": userId})
        expired_date = datetime.fromisoformat(account['AccountOwner']['Card']['ExpiredDate']).date()
        return render_template("viewProfile.html", account = account, expired_date = expired_date)
    elif request.method == "POST":
        return Response("changed something")

@account_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("account.login"))

@account_blueprint.route('/confirm_email', methods=['GET', 'POST'])
def confirm_email():
    if request.method == 'POST':
        user_email = request.form.get('email')
        # verify if user exist, send reset password page to the user's email
        exist_user = users.find_one({'Email': user_email})

        if exist_user is None:
            flash(messages['invalid_email'].format(user_email), 'error')
            return render_template('confirm_email.html')
        
        token = get_token(user_email, salt=app.salt)
        subject = "Reset Password"
        recover_url = url_for('account.reset_password',token=token, _external=True)
        html = render_template('email/activate.html',recover_url=recover_url)
        attachments = [{'path': './static/img/bank.png', 'filename':'bank.png', 'mime_type': 'image/png'}]
        send_email(user_email, subject, html, attachments=attachments)
        flash(messages['link_sent'].format(user_email), 'success')
        return redirect(url_for('account.login'))
    return render_template('confirm_email.html')


@account_blueprint.route('/reset_password/<token>', methods=["GET", "POST"])
def reset_password(token):
    if request.method == 'POST':
        try:
            user_email = ts.loads(token, salt=app.salt, max_age=86400)
            new_password = generate_password_hash(request.form.get('password'))
            exist_user = users.find_one({'Email': user_email},{'_id':0})

            update_password = accounts.update_one(
                {'AccountOwner': exist_user},
                {"$set": {"Password": new_password}
            })
                
            # Check if the update was successful
            if update_password.modified_count > 0:
                flash(messages['update_success'].format('password'), 'success')
                return redirect(url_for('account.login'))
                
            flash(messages['not_found'], 'error')
            return redirect(url_for('account.reset_password', token=token))
        except:
            flash(messages['token_expired'], 'error')
            return redirect(url_for('account.login'))
    return render_template('reset_password.html', token=token)

