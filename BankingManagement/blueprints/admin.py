from flask import Blueprint, render_template, request, jsonify

from models import database, account as a, user as u, branch as b

from helpers import login_required, paginator
from enums.role_type import RoleType
import random

admin_blueprint = Blueprint('admin', __name__)   

db = database.Database().get_db()
accounts = db['accounts']
users = db['users']
branches = db['branches']
cards = db['cards']
transferMethods = db['transferMethods']
loginMethods = db['loginMethods']
services = db['services']
employees = db['employees']

def create_random_user(i):
    return {
        "name": f"User {i}",
        "sex": random.choice([0, 1]),
        "address": f"Address {i}",
        "phone": f"000-000-000{i}",
        "email": f"user{i}@example.com",
        "card": []
    }

def create_random_branch(i):
    return {
        "branchName": f"Branch {i}",
        "address": f"Branch Address {i}"
    }

def create_account_list(num_accounts=30):
    accounts = []
    for i in range(num_accounts):
        user = u.User(**create_random_user(i)).to_json()
        branch = b.Branch(**create_random_branch(i)).to_json()
        acc = a.Account(
            accountNumber=f"00000000000{i:04}",
            branch=branch,
            user=user,
            username=f"user{i}",
            password="password123",
            role=RoleType.USER.value,
            transferMethod=["method1", "method2"],
            loginMethod=["login1", "login2"],
            service=["service1", "service2"]
        ).to_json()
        accounts.append(acc)
    return accounts

items = create_account_list()

@admin_blueprint.route('/admin/user', methods = ['GET'])
def admin_user():
    if request.method == 'GET':
        return render_template('admin/user.html')
    
@admin_blueprint.route('/admin/account', methods = ['GET'])
@login_required
def account():
    if request.method == 'GET':
        return render_template('admin/account.html')
    
@admin_blueprint.route('/admin/employee', methods = ['GET'])
def employee():
    if request.method == 'GET':
        return render_template('admin/employee.html')
    
@admin_blueprint.route('/admin/branch', methods = ['GET'])
def branch():
    if request.method == 'GET':
        return render_template('admin/branch.html')
    
@admin_blueprint.route('/admin/chart', methods = ['GET'])
def chart():
    if request.method == 'GET':
        return render_template('admin/chart.html')
    
@admin_blueprint.route('/admin/news', methods = ['GET'])
def news():
    if request.method == 'GET':
        return render_template('admin/news.html')
    
@admin_blueprint.route('/admin', methods=['GET'])
@login_required
def admin():
    page = request.args.get('page', 1, int)
    dataType = request.args.get('dataType')

    
    # This block of code will be use to request for data
    # items = []
    # if dataType == 'account':
    #     items = list(accounts.find({}, {'_id': 0})) 
    # elif dataType == 'user':
    #     items = list(users.find({}, {'_id': 0}))
    # elif dataType == 'branch':
    #     items = list(branches.find({}, {'_id': 0}))
    # elif dataType == 'employee':
    #     items = list(employees.find({}, {'_id': 0}))
    

    pagination = paginator(page, items)

    return jsonify({'items': pagination['render_items'], 'total_pages': pagination['total_pages']})