import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import account, user, card as model_card , database
from message import messages
from helpers import issueNewCard
db = database.Database().get_db()
accounts = db['accounts']
users = db['users']
branches = db['branches']
cards = db['cards']
transferMethods = db['transferMethods']
loginMethods = db['loginMethods']
services = db['services']
account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # get the data from post request
        username = request.form['username']
        fullName = request.form['fullName']
        branch = request.form['branch']
        password = request.form['password']
        address = request.form['address']
        transferMethod = request.form['transferMethod']
        confirmPassword = request.form['confirmPassword']
        phone = request.form['phone']
        loginMethod = request.form['loginMethod']
        email = request.form['email']
        sex = request.form['sex']
        service = request.form['service']
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

        # insert the document to the collection if there is no error
        if error is None:
            # get the date and expiry date of new card, insert new card into database
            today = datetime.date.today()
            cardExp = today.month,int(str(today.year+3)[2:])
            new_card = model_card.Card(cardNumber=card, cvv=cvvNumber, expiredDate=cardExp, issuanceDate=today)
            cards.insert_one(new_card.to_json())

            # insert new user into database
            new_user = user.User(name=fullName, sex=sex, address=address, phone=phone, email=email, card=new_card)
            users.insert_one(new_user.to_json())

            # insert new account into database
            new_account = account.Account(accountNumber=accountNumber, branch=branch, user=new_user, 
                                          username=username, password=password, role=0, transferMethod=[transferMethod], 
                                          loginMethod=[loginMethod], service=[service])
            accounts.insert_one(new_account.to_json())
            return redirect(url_for("account.register"))
                
        flash(error)
    elif request.method == 'GET':
        branch_list = branches.find()
        loginMethod_list = loginMethods.find()
        transferMethod_list = transferMethods.find()
        service_list = services.find()
        card_infor = issueNewCard()
        return render_template('register.html', branch_list=branch_list, loginMethod_list=loginMethod_list,
                               transferMethod_list=transferMethod_list, service_list=service_list, card_infor=card_infor)
