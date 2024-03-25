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
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']
        accountNumber = ' '
        branch = ' '
        accountOwner = ' '
        loginMethod = [ ]
        transferMethod = [ ]
        service = [ ]
        Sex=' '
        Address=' '
        Phone=' '
        Card=[ ]

        # check if user input email and password or not
        error = None
        if not email:
            error = 'email is required.'
        elif not username:
            error = 'username is required.'
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
            acc = account.Account(accountNumber, branch, accountOwner, username, password, 
                                  loginMethod, transferMethod, service)
            client = user.User(username, Sex, Address, Phone, email, Card)
            account_collection.insert_one(acc.to_json())
            user_collection.insert_one(client.to_json())
            return redirect(url_for("account.register"))
                
        flash(error)
    return render_template('register.html')
