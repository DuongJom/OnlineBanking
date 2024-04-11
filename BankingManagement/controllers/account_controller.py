from flask import flash, Blueprint, render_template, request, redirect, session, url_for, current_app
from werkzeug.security import check_password_hash, generate_password_hash
import json

from models import database, user, account
from message import messages

db = database.Database().get_db()

accounts = db['accounts']
users = db['users']
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
            flash(messages["invalid_information"])
            return redirect(url_for('account.login'))
        
        if not check_password_hash(acc["Password"], password):
            print("Sai mật khẩu")
            flash(messages['invalid_information'])
            return redirect(url_for('account.login'))
        
        if remember_me:
            session.permanent = True
            current_app.config['PERMANENT_SESSION_LIFETIME'] = 1209600  # 2 weeks in seconds
            session["userId"] = str(acc["_id"])
        else:
            session.permanent = False
            session["userId"] = str(acc["_id"])
        return redirect("/")
                
    return render_template('login.html')

# @account_blueprint.route('/create', methods=['GET', 'POST'])
# def create():
#     if request.method == 'POST':
#         # create user
#         Name = "Dang Huu Hieu"
#         Sex = 0
#         Phone = "0523370115"
#         Email = "huuhieu01@gmail.com"
#         Card = "083564571234"
#         Address =  "Thu Duc, Ho Chi Minh"

#         u = user.User(name=Name, sex=Sex, phone=Phone, email=Email, card=Card, address=Address)

#         user_document = json.loads(u.to_json()) 
#         users.insert_one(user_document)

#         AccountNumber = "6454649416421005"
#         Branch = "Ho Chi Minh"
#         AccountOwner = json.loads(u.to_json())
#         Username = "HuuHieu"
#         Password = request.form.get('hehe')

#         a = account.Account(accountNumber=AccountNumber, branch=Branch, user=AccountOwner, username=Username, password=Password) 

#         acc_doc = json.loads(a.to_json())
#         accounts.insert_one(acc_doc)

#         return redirect('/create')

#     return render_template("viewProfile.html")