from flask import flash, Blueprint, render_template, request, redirect, session, url_for, current_app
from werkzeug.security import check_password_hash

from models import database
from message import messages

db = database.Database().get_db()

collection = db['accounts']
account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.clear()
        username = request.form.get("username")
        password = request.form.get("password") 
        remember_me = request.form.get("remember_me")
        acc = collection.find_one({"Username": username}) 

        if acc is None:
            flash(messages["invalid_information"])
            return redirect(url_for('account.login')) 
        elif not check_password_hash(acc["Password"], password):
            flash(messages['invalid_information'])
            return redirect(url_for('account.login'))
        else:
            if remember_me:
                session.permanent = True
                current_app.config['PERMANENT_SESSION_LIFETIME'] = 1209600 
                session["userId"] = str(acc["_id"])
            else:
                session.permanent = False
                session["userId"] = str(acc["_id"])
            return redirect("/")
    return render_template('login.html')