from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash
from models import account, database
from util.security import ts, send_email

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

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@account_blueprint.route('/reset_email', methods=['GET', 'POST'])
def reset_email():
    if request.method == 'POST':
        user_email = request.form.get('email')
        # verify if user exist, send reset password page to the user's email
        user = collection.find_one({'email': user_email})
        if user:
            subject = "Password reset"
            # dumps convert python object to JSON string
            token = ts.dumps(user_email, salt='recover-key')
            recover_url = url_for('account.reset_with_token',token=token, _external=True)
            html = render_template('email/activate.html',recover_url=recover_url)
            send_email(user_email, subject, html)
        else:
            flash('User not exist')
            return render_template('reset_email.html')
        return redirect(url_for('account.reset_email'))
    return render_template('reset_email.html')


@account_blueprint.route('/reset_with_token/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    try:
       email=ts.loads(token, salt='recover_key',  max_age=86400)
    except:
        flash('Token expired')
        return redirect(url_for('account.login'))

    if request.method == 'POST':
        password = generate_password_hash(request.form.get('password'))# SERVER ERROR HERE
        collection.find_one_and_update(
            {'email': email},
            {'$set':
                {'password': password}
            },upsert=False
        ) 
        return redirect(url_for('account.login'))