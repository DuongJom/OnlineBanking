from flask import (Blueprint, render_template, request, redirect, url_for, flash)
from models import account, database

db = database.Database().get_db()
collection = db['accounts']
account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        pass
    return render_template('login.html')

@account_blueprint.route('/logout', methods=['POST'])
def logout():
    pass

@account_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # get the data from post request
        email = request.form['email']
        print(email)
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']

        # check if user input email and password or not
        error = None
        if not email:
            error = 'email is required.'
        elif not password:
            error = 'Password is required.'
        elif password != confirmPassword:
            error = 'Confirmation password does not match'
        # check if email already exist
        existEmail = collection.find_one({"email": email})
        print(existEmail)
        if existEmail != None:
            error = f"Email {email} is already registered." 
        # insert the document to the collection if there is no error
        if error is None:
            acc = account.Account(email=email, password=password)
            collection.insert_one(acc.to_json())
            return redirect(url_for("account.login"))
                
        flash(error)
    return render_template('register.html')

