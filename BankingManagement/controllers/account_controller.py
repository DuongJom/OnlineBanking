from flask import Blueprint, render_template, request, redirect, jsonify
from werkzeug.security import check_password_hash

from models import account, database
from controllers.home_controller import home_blueprint
from message import messages

db = database.Database().get_db()

collection = db['accounts']
account_blueprint = Blueprint('account', __name__)

@account_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password") 
        account = collection.find_one({"Username": username})  

        if account:
            if check_password_hash(account["Password"], password):
                return jsonify({'message': messages['login_success']})
            return jsonify({'message': 'Invalid username or password'})
        
        return jsonify({"message": "account is not found"})
    elif request.method == "GET" :
        return render_template('login.html')
    

@account_blueprint.route('/logout', methods=['POST'])
def logout():
    pass

@account_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        try:
            acc = account.Account(email="admin123@gmail.com", password="admin123@")
            collection.insert_one(acc.to_json())
            return redirect('/login')
        except:
            return
    return render_template('register.html')