from flask import Blueprint, render_template, request, redirect
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
        try:
            acc = account.Account(email="admin123@gmail.com", password="admin123@")
            collection.insert_one(acc.to_json())
            return redirect('/login')
        except:
            return
    return render_template('register.html')
