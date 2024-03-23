from flask import Blueprint, render_template, request, redirect, session
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
        acc = collection.find_one({"Username": username})  

        if acc is None:
            return render_template("login.html", message = messages['invalid_information'])
        elif not check_password_hash(acc["Password"], password):
            return render_template("login.html", message = messages['invalid_information'])
        
        session["userId"] = str(acc["_id"])
        return redirect("/")
        
    elif request.method == "GET" :
        return render_template('login.html')