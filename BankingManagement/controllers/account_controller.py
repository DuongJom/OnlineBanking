from flask import Blueprint, session, render_template, request, redirect, url_for, flash

from models import account, database, email

db = database.Database().get_db()
collection = db['accounts']
account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        # get the data from post request
        email = request.form['email']
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
        if existEmail:
            error = f"Email {email} is already registered." 
        # insert the document to the collection if there is no error
        if error is None:
            acc = account.Account(email,password)
            collection.insert_one(acc.to_json())
            return redirect(url_for("account.login"))
                
        flash(error)
    return render_template('register.html')

@account_blueprint.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("account.login"))

@account_blueprint.route('/reset_password', methods=['GET', 'POST'])
def resetPassword():
    if request.method == 'POST':
        user_email = request.form.get('email')

        # verify if user exist, send reset password page to the user's email
        user = collection.find_one({'Email': user_email})
        if user:
            email.send_email(user)

        return redirect(url_for("account.login"))

    return render_template('reset_password.html')

@account_blueprint.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_verified(token):
    if request.method == 'POST':
        password = request.form['password']
        confirmPassword = request.form['confirmPassword']