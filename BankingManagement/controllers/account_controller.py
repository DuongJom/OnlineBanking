from flask import Blueprint, render_template, request, redirect, url_for, flash

from models import account, user, database

db = database.Database().get_db()
account_collection = db['accounts']
user_collection = db['users']
account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # get the data from post request
        email = request.form['Email']
        username = request.form['Username']
        password = request.form['Password']
        confirmPassword = request.form['confirmPassword']
        accountNumber = ''
        branch = request.form['Branch']
        accountOwner = request.form['AccountOwner']
        loginMethod = request.form['LoginMethod']
        transferMethod = request.form['TransferMethod']
        service = request.form['Service']
        sex = request.form['Sex']
        address = request.form['Address']
        phone = request.form['Phone']
        card = request.form['Card']

        # check if user input email and password or not
        error = None
        if not email:
            error = 'Email is required.'
        elif not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmPassword:
            error = 'Confirmation password does not match'

        # check if email or username already exist
        existUsername = account_collection.find_one({"Username": username})
        existEmail = user_collection.find_one({"Email": email})
        if existUsername:
            error = f"Username {username} is already registered." 
        elif existEmail:
            error = f"Email {email} is already registered." 

        # insert the document to the collection if there is no error
        if error is None:
            new_account = account.Account(AccountNumber=accountNumber, Branch=branch, AccountOwner=accountOwner, Username=username, Password=password, 
                                  TransferMethod=[transferMethod], LoginMethod=[loginMethod], Service=[service])
            new_user = user.User(Name=accountOwner, Sex=sex, Address=address, Phone=phone, Email=email, Card=card)
            account_collection.insert_one(new_account.to_json())
            user_collection.insert_one(new_user.to_json())
            return redirect(url_for("account.register"))
                
        flash(error)
    return render_template('register.html')